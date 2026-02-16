"""
Email action router for handling Approve/Regenerate/Decline from email buttons.

These are GET endpoints (because email buttons are <a href> links) that
process the action, trigger side effects, and redirect to a frontend page.

This flow is the email fallback equivalent of WhatsApp's interactive buttons.
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from backend.config import get_settings
from backend.models.schemas import SubmissionStatus
from backend.services import sheets_service, email_service, gemini_service
from backend.utils.logger import logger

router = APIRouter(prefix="/api/email-action", tags=["Email Actions"])

# Terminal statuses — once in these states, no further action is allowed
TERMINAL_STATUSES = {
    SubmissionStatus.DECLINED.value,
    SubmissionStatus.COPIED.value,
    SubmissionStatus.POSTED.value,
}


@router.get("/{token}/{action}")
async def handle_email_action(token: str, action: str):
    """
    Process an email action button click (approve, regenerate, or decline).

    Args:
        token: Consent token identifying the submission.
        action: One of 'approve', 'regenerate', 'decline'.

    Returns:
        RedirectResponse to the appropriate frontend page.
    """
    settings = get_settings()
    sheet_id = settings.FORM_RESPONSES_SHEET_ID

    if action not in ("approve", "regenerate", "decline"):
        raise HTTPException(status_code=400, detail="Invalid action")

    if not sheet_id:
        raise HTTPException(status_code=500, detail="Sheet not configured")

    # Fetch full submission data
    submission = await sheets_service.get_full_submission_by_token(sheet_id, token)

    if not submission:
        logger.warning(f"Email action: token not found — {token[:8]}...")
        return RedirectResponse(
            f"{settings.FRONTEND_URL}/action-confirmed?type=expired",
            status_code=302,
        )

    # Check token expiry
    sent_at_str = submission.get("sent_at", "")
    if sent_at_str:
        try:
            sent_at = datetime.strptime(sent_at_str, "%Y-%m-%d %H:%M:%S")
            days_elapsed = (datetime.now() - sent_at).days
            if days_elapsed > settings.CONSENT_TOKEN_EXPIRY_DAYS:
                logger.warning(f"Email action: token expired for {token[:8]}...")
                return RedirectResponse(
                    f"{settings.FRONTEND_URL}/action-confirmed?type=expired",
                    status_code=302,
                )
        except ValueError:
            pass

    # Check terminal status
    current_status = submission.get("status", "").upper()
    if current_status in TERMINAL_STATUSES:
        logger.info(f"Email action: already actioned ({current_status}) for {token[:8]}...")
        return RedirectResponse(
            f"{settings.FRONTEND_URL}/action-confirmed?type=already-actioned",
            status_code=302,
        )

    row = submission["row"]
    client_name = submission.get("client_name", "Valued Client")
    client_email = submission.get("business_email") or submission.get("email", "")

    if not client_email:
        logger.error(f"Email action: no email for {token[:8]}...")
        raise HTTPException(status_code=400, detail="No email address on file")

    # ─── Approve ────────────────────────────────────────
    if action == "approve":
        return await _handle_approve(
            settings, sheet_id, row, token, client_name, client_email
        )

    # ─── Regenerate ─────────────────────────────────────
    if action == "regenerate":
        return await _handle_regenerate(
            settings, sheet_id, row, token, client_name, client_email, submission
        )

    # ─── Decline ────────────────────────────────────────
    return await _handle_decline(
        settings, sheet_id, row, token, client_name, client_email
    )


# ─── Action Handlers ─────────────────────────────────────


async def _handle_approve(settings, sheet_id, row, token, client_name, client_email):
    """Approve the review and send landing page link."""
    landing_url = f"{settings.FRONTEND_URL}/review/{token}"

    # Update sheet status
    await sheets_service.update_submission_row(sheet_id, row, {
        "status": SubmissionStatus.APPROVED.value,
    })

    # Send approval email with landing page link
    await email_service.send_approval_email(
        to_email=client_email,
        client_name=client_name,
        landing_page_url=landing_url,
    )

    # Log audit event
    await sheets_service.log_audit_event(
        sheet_id, "EMAIL_APPROVED", f"row_{row}",
        f"Client {client_name} approved review via email."
    )

    logger.info(f"Email action: APPROVED for row {row} ({client_name})")

    # Redirect to the landing page directly
    return RedirectResponse(landing_url, status_code=302)


async def _handle_regenerate(
    settings, sheet_id, row, token, client_name, client_email, submission
):
    """Regenerate a new AI draft and send it via email."""
    regen_count = submission.get("regen_count", 0)

    # Check regeneration limit
    if regen_count >= settings.MAX_REGENERATIONS:
        logger.warning(f"Email action: regen limit reached for {token[:8]}...")
        return RedirectResponse(
            f"{settings.FRONTEND_URL}/action-confirmed?type=regen-limit",
            status_code=302,
        )

    # Build ratings breakdown from stored form data
    ratings_breakdown = {
        "q1": submission.get("q1"),
        "q2": submission.get("q2"),
        "q3": submission.get("q3"),
        "q4": submission.get("q4"),
        "q5": submission.get("q5"),
        "q6": submission.get("q6"),
        "q7": submission.get("q7"),
        "q8": submission.get("q8"),
    }

    avg_rating = submission.get("avg_rating") or 0.0

    try:
        # Generate new draft
        new_draft = await gemini_service.generate_review_draft(
            client_name=client_name,
            company=submission.get("company", ""),
            services=submission.get("services", ""),
            avg_rating=avg_rating,
            ratings_breakdown=ratings_breakdown,
            open_feedback=submission.get("q10_open_feedback", ""),
        )
    except Exception as e:
        logger.error(f"Regeneration failed for {token[:8]}...: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate new draft")

    new_regen_count = regen_count + 1

    # Update sheet with new draft and incremented regen count
    await sheets_service.update_submission_row(sheet_id, row, {
        "draft_text": new_draft,
        "regen_count": new_regen_count,
        "status": SubmissionStatus.SENT.value,
    })

    # Build action URLs for the new email
    base_url = f"{settings.APP_BASE_URL}/api/email-action/{token}"
    approve_url = f"{base_url}/approve"
    decline_url = f"{base_url}/decline"

    # Only include regenerate URL if limit not yet reached
    regenerate_url = None
    if new_regen_count < settings.MAX_REGENERATIONS:
        regenerate_url = f"{base_url}/regenerate"

    # Send new draft email
    await email_service.send_regenerated_email(
        to_email=client_email,
        client_name=client_name,
        draft_text=new_draft,
        approve_url=approve_url,
        regenerate_url=regenerate_url,
        decline_url=decline_url,
        regen_count=new_regen_count,
    )

    # Log audit event
    await sheets_service.log_audit_event(
        sheet_id, "EMAIL_REGENERATED", f"row_{row}",
        f"Client {client_name} requested regeneration ({new_regen_count}/{settings.MAX_REGENERATIONS})."
    )

    logger.info(
        f"Email action: REGENERATED for row {row} "
        f"({new_regen_count}/{settings.MAX_REGENERATIONS})"
    )

    return RedirectResponse(
        f"{settings.FRONTEND_URL}/action-confirmed?type=regenerate",
        status_code=302,
    )


async def _handle_decline(settings, sheet_id, row, token, client_name, client_email):
    """Decline the review and send thank-you email."""
    # Update sheet status
    await sheets_service.update_submission_row(sheet_id, row, {
        "status": SubmissionStatus.DECLINED.value,
    })

    # Send decline thank-you email
    await email_service.send_decline_email(
        to_email=client_email,
        client_name=client_name,
    )

    # Log audit event
    await sheets_service.log_audit_event(
        sheet_id, "EMAIL_DECLINED", f"row_{row}",
        f"Client {client_name} declined review via email."
    )

    logger.info(f"Email action: DECLINED for row {row} ({client_name})")

    return RedirectResponse(
        f"{settings.FRONTEND_URL}/action-confirmed?type=decline",
        status_code=302,
    )
