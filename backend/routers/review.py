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

    review_data = sheets_service.get_review_by_token(sheet_id, token)

    if not review_data:
        logger.warning(f"Review not found for token: {token[:8]}...")
        raise HTTPException(
            status_code=404,
            detail="Review not found or link has expired.",
        )

    return ReviewResponse(
        draft_text=review_data.get("draft_text", ""),
        client_name=review_data.get("client_name", "Valued Client"),
        gbp_review_url=settings.GBP_REVIEW_URL,
        status=review_data.get("status", SubmissionStatus.PENDING.value),
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

    review_data = sheets_service.get_review_by_token(sheet_id, token)

    if not review_data:
        raise HTTPException(status_code=404, detail="Review not found")

    row = review_data["row"]

    from datetime import datetime

    sheets_service.update_submission_row(sheet_id, row, {
        "status": SubmissionStatus.COPIED.value,
        "copied_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    sheets_service.log_audit_event(
        sheet_id, "REVIEW_COPIED", f"row_{row}",
        "Client copied review text from landing page."
    )

    logger.info(f"Review copied for row {row}")

    return {"success": True, "message": "Copy event recorded"}
