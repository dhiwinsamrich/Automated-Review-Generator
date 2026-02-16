"""
Review API router.

Serves review data for the React landing page.
"""

from datetime import datetime

from fastapi import APIRouter, Header, HTTPException

from backend.config import get_settings
from backend.models.schemas import ReviewResponse, SubmissionStatus, ClientData
from backend.services import sheets_service, notification_service
from backend.utils.logger import logger

router = APIRouter(prefix="/api", tags=["Review"])


@router.get("/review/{token}", response_model=ReviewResponse)
async def get_review(token: str):
    """
    Get review data by consent token.

    Called by the React landing page to display the review draft
    and provide the GBP review URL for redirect.

    Args:
        token: Unique consent token from the WhatsApp/email link.

    Returns:
        ReviewResponse with draft text, client name, and GBP URL.
    """
    settings = get_settings()
    sheet_id = settings.FORM_RESPONSES_SHEET_ID

    if not sheet_id:
        raise HTTPException(
            status_code=500,
            detail="FORM_RESPONSES_SHEET_ID not configured",
        )

    review_data = await sheets_service.get_review_by_token(sheet_id, token)

    if not review_data:
        logger.warning(f"Review not found for token: {token[:8]}...")
        raise HTTPException(
            status_code=404,
            detail="Review not found or link has expired.",
        )

    # Check token expiration
    sent_at_str = review_data.get("sent_at", "")
    if sent_at_str:
        try:
            sent_at = datetime.strptime(sent_at_str, "%Y-%m-%d %H:%M:%S")
            days_elapsed = (datetime.now() - sent_at).days
            if days_elapsed > settings.CONSENT_TOKEN_EXPIRY_DAYS:
                logger.warning(
                    f"Token expired for {token[:8]}... "
                    f"({days_elapsed} days > {settings.CONSENT_TOKEN_EXPIRY_DAYS})"
                )
                raise HTTPException(
                    status_code=410,
                    detail="This review link has expired. Please contact us for a new one.",
                )
        except ValueError:
            pass  # If date parsing fails, allow access

    # Parse rating: avg_rating is a float like 9.5 (out of 10), convert to 1-5 stars
    avg_rating_str = review_data.get("avg_rating", "")
    try:
        avg_rating = float(avg_rating_str) if avg_rating_str else 10.0
        rating = max(1, min(5, round(avg_rating / 2)))
    except (ValueError, TypeError):
        rating = 5

    # Parse regeneration count
    regen_str = review_data.get("regen_count", "")
    try:
        regen_count = int(regen_str) if regen_str else 0
    except (ValueError, TypeError):
        regen_count = 0

    return ReviewResponse(
        draft_text=review_data.get("draft_text", ""),
        client_name=review_data.get("client_name", "Valued Client"),
        business_name=review_data.get("company", "") or "Our Business",
        rating=rating,
        gbp_review_url=settings.GBP_REVIEW_URL,
        status=review_data.get("status", SubmissionStatus.PENDING.value),
        regeneration_count=regen_count,
        max_regenerations=settings.MAX_REGENERATIONS,
    )


@router.post("/review/{token}/copied")
async def mark_review_copied(token: str):
    """
    Mark a review as copied by the client.

    Called by the landing page when the client clicks "Copy & Post Review".
    Updates the sheet status to track conversion.

    Args:
        token: Consent token for the review.
    """
    settings = get_settings()
    sheet_id = settings.FORM_RESPONSES_SHEET_ID

    review_data = await sheets_service.get_review_by_token(sheet_id, token)

    if not review_data:
        raise HTTPException(status_code=404, detail="Review not found")

    row = review_data["row"]

    await sheets_service.update_submission_row(sheet_id, row, {
        "status": SubmissionStatus.COPIED.value,
        "copied_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    await sheets_service.log_audit_event(
        sheet_id, "REVIEW_COPIED", f"row_{row}",
        "Client copied review text from landing page."
    )

    logger.info(f"Review copied for row {row}")

    return {"success": True, "message": "Copy event recorded"}


@router.post("/reviews/send-reminders", tags=["System"])
async def send_pending_reminders(
    x_webhook_secret: str = Header(default="", alias="X-Webhook-Secret"),
):
    """
    Send reminder notifications for approved-but-not-copied reviews.

    Call this endpoint via an external scheduler (cron, Cloud Scheduler)
    to nudge clients who approved but haven't posted yet.

    Requires the webhook secret header for authentication.
    """
    settings = get_settings()

    if settings.WEBHOOK_SECRET and x_webhook_secret != settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid webhook secret")

    sheet_id = settings.FORM_RESPONSES_SHEET_ID
    if not sheet_id:
        return {"success": False, "message": "FORM_RESPONSES_SHEET_ID not configured"}

    reminded = 0
    expired = 0

    try:
        import asyncio
        all_data = await asyncio.to_thread(
            _get_all_rows_sync, sheet_id
        )

        from backend.services.sheets_service import COLUMN_MAP, _col_letter_to_num, _safe_get

        status_col = _col_letter_to_num(COLUMN_MAP["status"]) - 1
        sent_at_col = _col_letter_to_num(COLUMN_MAP["sent_at"]) - 1
        token_col = _col_letter_to_num(COLUMN_MAP["token"]) - 1
        name_col = _col_letter_to_num(COLUMN_MAP["client_name"]) - 1
        wa_col = _col_letter_to_num(COLUMN_MAP["whatsapp"]) - 1
        email_col = _col_letter_to_num(COLUMN_MAP["business_email"]) - 1

        for row_data in all_data[1:]:  # Skip header
            status = _safe_get(row_data, status_col).upper()
            if status not in ("SENT", "APPROVED"):
                continue

            sent_at_str = _safe_get(row_data, sent_at_col)
            if not sent_at_str:
                continue

            try:
                sent_at = datetime.strptime(sent_at_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            days_elapsed = (datetime.now() - sent_at).days

            # Expire if past token expiry
            if days_elapsed > settings.CONSENT_TOKEN_EXPIRY_DAYS:
                expired += 1
                continue

            # Send reminder if 3+ days old
            if days_elapsed >= 3:
                token = _safe_get(row_data, token_col)
                client_name = _safe_get(row_data, name_col) or "Valued Client"
                whatsapp = _safe_get(row_data, wa_col)
                business_email = _safe_get(row_data, email_col)

                if not token:
                    continue

                client_data = ClientData(
                    name=client_name,
                    whatsapp=whatsapp or None,
                    business_email=business_email,
                )

                await notification_service.send_approval_notification(
                    client_data=client_data,
                    token=token,
                )
                reminded += 1

    except Exception as e:
        logger.error(f"Reminder job failed: {e}")
        return {"success": False, "message": str(e)}

    logger.info(f"Reminder job complete: {reminded} reminded, {expired} expired")
    return {
        "success": True,
        "reminded": reminded,
        "expired": expired,
    }


def _get_all_rows_sync(sheet_id: str) -> list:
    """Fetch all rows from the form responses sheet (sync helper)."""
    from backend.services.sheets_service import _get_client
    client = _get_client()
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet.get_all_values()
