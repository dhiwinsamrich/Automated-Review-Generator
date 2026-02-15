"""
Form submission webhook router.

Receives POST requests from the Google Apps Script trigger
when a new form submission is logged in Google Sheets.

This is the main entry point for the entire review generation pipeline.
"""

import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Header

from backend.config import get_settings
from backend.models.schemas import (
    FormSubmissionData,
    WebhookResponse,
    SubmissionStatus,
)
from backend.services import (
    qualification,
    sheets_service,
    gemini_service,
    notification_service,
)
from backend.utils.logger import logger

router = APIRouter(prefix="/api/webhook", tags=["Webhooks"])


@router.post("/form", response_model=WebhookResponse)
async def handle_form_submission(
    submission: FormSubmissionData,
    x_webhook_secret: str = Header(default="", alias="X-Webhook-Secret"),
):
    """
    Process a new Google Form submission.

    Pipeline:
    1. Validate webhook secret
    2. Check for duplicate submissions
    3. Look up client in CRM sheet by email
    4. Calculate average rating from Q1-Q8
    5. Check qualification (avg >= threshold AND consent = Yes)
    6. If qualified: generate AI draft → send WhatsApp/email
    7. If not qualified: send internal alert (context-aware)
    8. Update form responses sheet with status

    Args:
        submission: Form data forwarded by Google Apps Script.
        x_webhook_secret: Secret header for webhook authentication.

    Returns:
        WebhookResponse with processing result.
    """
    settings = get_settings()

    # Step 0: Validate webhook secret
    if settings.WEBHOOK_SECRET:
        if x_webhook_secret != settings.WEBHOOK_SECRET:
            logger.warning(
                f"Webhook auth failed for row {submission.row_number} "
                f"from {submission.email}"
            )
            raise HTTPException(status_code=403, detail="Invalid webhook secret")

    sheet_id = submission.sheet_id or settings.FORM_RESPONSES_SHEET_ID
    row = submission.row_number

    logger.info(f"Processing form submission: row={row}, email={submission.email}")

    try:
        # Step 1: Check for duplicate active submissions
        is_duplicate = await sheets_service.check_duplicate_submission(
            sheet_id, submission.email
        )
        if is_duplicate:
            logger.info(f"Duplicate submission detected for {submission.email}")
            await sheets_service.log_audit_event(
                sheet_id, "DUPLICATE", f"row_{row}",
                f"Duplicate submission from {submission.email} — skipping"
            )
            return WebhookResponse(
                success=True,
                message="Duplicate submission detected. Previous submission is still active.",
                data={"duplicate": True},
            )

        # Step 2: Look up client in CRM
        client_data = await sheets_service.lookup_client_by_email(submission.email)

        # Write CRM data back to sheet
        await sheets_service.update_submission_row(sheet_id, row, {
            "client_name": client_data.name,
            "company": client_data.company,
            "services": client_data.services,
            "whatsapp": client_data.whatsapp or "",
            "business_email": client_data.business_email,
        })

        await sheets_service.log_audit_event(
            sheet_id, "FORM_SUBMIT", f"row_{row}",
            f"New submission from {submission.email} "
            f"(CRM match: {client_data.found})"
        )

        # Step 3: Calculate qualification
        avg_rating = qualification.calculate_average(submission.ratings)
        rating_ok = qualification.meets_rating_threshold(avg_rating)
        consent_ok = qualification.has_testimonial_consent(
            submission.q9_testimonial_consent
        )
        is_qualified = rating_ok and consent_ok

        # Check for negative sentiment in open feedback (edge case EC-01)
        sentiment_flag = qualification.has_negative_sentiment(
            submission.q10_open_feedback or ""
        )

        # Write qualification data
        await sheets_service.update_submission_row(sheet_id, row, {
            "avg_rating": avg_rating,
            "qualified": "YES" if is_qualified else "NO",
        })

        # Step 4: Branch based on qualification
        if is_qualified and not sentiment_flag:
            result = await _process_qualified(
                sheet_id, row, submission, client_data, avg_rating
            )
        elif rating_ok and not consent_ok:
            # High rating but consent declined — different alert
            result = await _process_consent_declined(
                sheet_id, row, submission, client_data, avg_rating
            )
        else:
            # Low rating OR negative sentiment flagged
            result = await _process_unqualified(
                sheet_id, row, submission, client_data, avg_rating,
                sentiment_flag=sentiment_flag,
            )

        return WebhookResponse(
            success=True,
            message=result["message"],
            data=result.get("data"),
        )

    except Exception as e:
        logger.error(f"Pipeline error for row {row}: {e}")

        # Write error to sheet
        await sheets_service.update_submission_row(sheet_id, row, {
            "status": SubmissionStatus.PENDING.value,
            "error": str(e),
        })

        await sheets_service.log_audit_event(
            sheet_id, "ERROR", f"row_{row}", str(e)
        )

        raise HTTPException(status_code=500, detail=str(e))


async def _process_qualified(
    sheet_id: str,
    row: int,
    submission: FormSubmissionData,
    client_data,
    avg_rating: float,
) -> dict:
    """Handle a qualified submission: generate draft, send notification."""

    logger.info(f"Row {row}: QUALIFIED (avg={avg_rating})")

    sheets_service.log_audit_event(
        sheet_id, "QUALIFIED", f"row_{row}",
        f"Avg: {avg_rating}, Consent: Yes"
    )

    # Generate AI review draft
    draft = await gemini_service.generate_review_draft(
        client_name=client_data.name,
        company=client_data.company,
        services=client_data.services,
        avg_rating=avg_rating,
        ratings_breakdown=submission.ratings_breakdown,
        open_feedback=submission.q10_open_feedback or "",
    )

    # Generate unique consent token
    token = str(uuid.uuid4())

    # Write draft and token to sheet
    sheets_service.update_submission_row(sheet_id, row, {
        "draft_text": draft,
        "token": token,
        "status": SubmissionStatus.PENDING.value,
    })

    sheets_service.log_audit_event(
        sheet_id, "AI_DRAFT_GENERATED", f"row_{row}",
        f"Draft: {len(draft)} chars, Token: {token[:8]}..."
    )

    # Send notification (WhatsApp primary, email fallback)
    result = await notification_service.send_review_notification(
        client_data=client_data,
        draft_text=draft,
        token=token,
    )

    # Update delivery status
    sheets_service.update_submission_row(sheet_id, row, {
        "status": SubmissionStatus.SENT.value,
        "delivery_method": result.method.value,
        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    sheets_service.log_audit_event(
        sheet_id, "NOTIFICATION_SENT", f"row_{row}",
        f"Method: {result.method.value}, Success: {result.success}"
    )

    return {
        "message": f"Qualified submission processed. Notification sent via {result.method.value}.",
        "data": {
            "qualified": True,
            "avg_rating": avg_rating,
            "delivery_method": result.method.value,
            "token": token,
        },
    }


async def _process_unqualified(
    sheet_id: str,
    row: int,
    submission: FormSubmissionData,
    client_data,
    avg_rating: float,
) -> dict:
    """Handle an unqualified submission: send internal alert."""

    logger.info(
        f"Row {row}: NOT QUALIFIED "
        f"(avg={avg_rating}, consent={submission.q9_testimonial_consent})"
    )

    sheets_service.update_submission_row(sheet_id, row, {
        "status": SubmissionStatus.ALERT_SENT.value,
    })

    # Send internal alert
    await notification_service.send_low_rating_alert(
        client_data=client_data,
        avg_rating=avg_rating,
        open_feedback=submission.q10_open_feedback or "",
    )

    sheets_service.log_audit_event(
        sheet_id, "LOW_RATING_ALERT", f"row_{row}",
        f"Avg: {avg_rating}, Alert sent to internal team"
    )

    return {
        "message": "Low-rated submission. Internal alert sent.",
        "data": {
            "qualified": False,
            "avg_rating": avg_rating,
        },
    }
