"""
Notification orchestrator service.

Coordinates between WhatsApp (primary) and Email (fallback)
for sending review notifications to clients.
"""

from backend.config import get_settings
from backend.models.schemas import ClientData, DeliveryMethod, NotificationResult
from backend.services import whatsapp_service, email_service
from backend.utils.logger import logger


async def send_review_notification(
    client_data: ClientData,
    draft_text: str,
    token: str,
) -> NotificationResult:
    """
    Send the initial review consent notification to the client.

    Strategy: WhatsApp first (if number available), email fallback.

    This sends Message 1 — the review draft with Approve/Edit/Decline options.

    Args:
        client_data: Client details from CRM lookup.
        draft_text: AI-generated review draft.
        token: Unique consent token.

    Returns:
        NotificationResult with delivery method and success status.
    """
    # Step 1: Try WhatsApp if number is available
    if client_data.whatsapp:
        logger.info(f"Attempting WhatsApp delivery to {client_data.whatsapp}")

        wa_result = await whatsapp_service.send_consent_message(
            phone=client_data.whatsapp,
            client_name=client_data.name,
            draft_text=draft_text,
            token=token,
        )

        if wa_result["success"]:
            logger.info(f"WhatsApp consent message sent to {client_data.name}")
            return NotificationResult(
                method=DeliveryMethod.WHATSAPP,
                success=True,
                message_id=wa_result.get("message_id"),
            )

        logger.warning(
            f"WhatsApp failed for {client_data.name}: {wa_result.get('error')}. "
            f"Falling back to email."
        )

    # Step 2: Fallback to email
    landing_url = _build_landing_url(token)
    email_target = client_data.business_email

    if not email_target:
        logger.error(f"No email address available for {client_data.name}")
        return NotificationResult(
            method=DeliveryMethod.NONE,
            success=False,
            error="No contact method available",
        )

    logger.info(f"Sending email fallback to {email_target}")
    email_success = await email_service.send_consent_email(
        to_email=email_target,
        client_name=client_data.name,
        draft_text=draft_text,
        landing_page_url=landing_url,
    )

    if email_success:
        return NotificationResult(
            method=DeliveryMethod.EMAIL,
            success=True,
        )

    return NotificationResult(
        method=DeliveryMethod.NONE,
        success=False,
        error="Both WhatsApp and email delivery failed",
    )


async def send_approval_notification(
    client_data: ClientData,
    token: str,
) -> NotificationResult:
    """
    Send Message 2 after client approves the review.

    Contains a URL button/link to the landing page where
    they can copy the review and get redirected to GBP.

    Args:
        client_data: Client details from CRM.
        token: Consent token for the landing page URL.

    Returns:
        NotificationResult with delivery method and success status.
    """
    landing_url = _build_landing_url(token)

    # Try WhatsApp first
    if client_data.whatsapp:
        wa_result = await whatsapp_service.send_review_ready_message(
            phone=client_data.whatsapp,
            client_name=client_data.name,
            landing_page_url=landing_url,
        )

        if wa_result["success"]:
            logger.info(f"Review-ready message sent via WhatsApp to {client_data.name}")
            return NotificationResult(
                method=DeliveryMethod.WHATSAPP,
                success=True,
                message_id=wa_result.get("message_id"),
            )

    # Email fallback — same landing page URL
    if client_data.business_email:
        email_success = await email_service.send_consent_email(
            to_email=client_data.business_email,
            client_name=client_data.name,
            draft_text="Your approved review is ready to post!",
            landing_page_url=landing_url,
        )

        if email_success:
            return NotificationResult(method=DeliveryMethod.EMAIL, success=True)

    return NotificationResult(
        method=DeliveryMethod.NONE,
        success=False,
        error="Failed to send approval notification",
    )


async def send_low_rating_alert(
    client_data: ClientData,
    avg_rating: float,
    open_feedback: str = "",
    reason: str = "low_rating",
) -> bool:
    """
    Send internal alert email for low-rated or consent-declined submissions.

    Args:
        client_data: Client details.
        avg_rating: Average rating.
        open_feedback: Q10 open-text feedback.
        reason: Alert reason — 'low_rating', 'consent_declined', or 'negative_sentiment'.

    Returns:
        True if alert sent successfully.
    """
    return await email_service.send_internal_alert(
        client_name=client_data.name,
        company=client_data.company,
        avg_rating=avg_rating,
        open_feedback=open_feedback or "",
        reason=reason,
    )


# ─── Helper ──────────────────────────────────────────────


def _build_landing_url(token: str) -> str:
    """Build the landing page URL with the review token."""
    settings = get_settings()
    return f"{settings.FRONTEND_URL}/review/{token}"
