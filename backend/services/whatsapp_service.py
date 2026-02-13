"""
WhatsApp Business API service.

Sends messages via the official WhatsApp Cloud API (Meta).
Supports interactive messages with quick reply buttons and URL buttons.
"""

import httpx

from backend.config import get_settings
from backend.utils.logger import logger


async def send_consent_message(
    phone: str,
    client_name: str,
    draft_text: str,
    token: str,
) -> dict:
    """
    Send WhatsApp Message 1: Review draft with Approve/Edit/Decline buttons.

    Uses an interactive message with quick reply buttons so the client
    can respond directly within WhatsApp.

    Args:
        phone: Client's WhatsApp number in E.164 format.
        client_name: Client's name for personalization.
        draft_text: AI-generated review draft.
        token: Unique consent token for tracking.

    Returns:
        Dict with 'success', 'message_id', and optionally 'error'.
    """
    settings = get_settings()

    # Truncate draft for WhatsApp body (max ~1024 chars for interactive body)
    truncated_draft = _truncate(draft_text, 800)

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone.replace("+", ""),  # WhatsApp API expects number without +
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {
                "type": "text",
                "text": "Your Review Draft is Ready! 📝",
            },
            "body": {
                "text": (
                    f"Hi {client_name},\n\n"
                    f"Thank you for your feedback on our recent project! "
                    f"Based on your responses, we've drafted a review for you:\n\n"
                    f'"{truncated_draft}"\n\n'
                    f"Would you like to post this review on Google?"
                ),
            },
            "footer": {
                "text": "bdcode - Thank you for your partnership",
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"approve_{token}",
                            "title": "Approve ✅",
                        },
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"edit_{token}",
                            "title": "Edit ✏️",
                        },
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"decline_{token}",
                            "title": "Decline ❌",
                        },
                    },
                ],
            },
        },
    }

    return await _send_whatsapp_message(payload)


async def send_review_ready_message(
    phone: str,
    client_name: str,
    landing_page_url: str,
) -> dict:
    """
    Send WhatsApp Message 2: Confirmation with URL button to landing page.

    Sent after client taps "Approve" on Message 1.

    Args:
        phone: Client's WhatsApp number in E.164 format.
        client_name: Client's name for personalization.
        landing_page_url: Full URL to the copy+redirect landing page.

    Returns:
        Dict with 'success', 'message_id', and optionally 'error'.
    """
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone.replace("+", ""),
        "type": "interactive",
        "interactive": {
            "type": "cta_url",
            "header": {
                "type": "text",
                "text": "Your Review is Approved! 🎉",
            },
            "body": {
                "text": (
                    f"Great, {client_name}! Your review is ready.\n\n"
                    f"Tap below to copy and post — takes just 10 seconds! 🚀"
                ),
            },
            "footer": {
                "text": "bdcode - Thank you for your partnership",
            },
            "action": {
                "name": "cta_url",
                "parameters": {
                    "display_text": "📋 Copy & Post Review",
                    "url": landing_page_url,
                },
            },
        },
    }

    return await _send_whatsapp_message(payload)


async def send_reminder_message(
    phone: str,
    client_name: str,
    landing_page_url: str,
) -> dict:
    """
    Send a follow-up reminder for approved but not-yet-posted reviews.

    Args:
        phone: Client's WhatsApp number.
        client_name: Client's name.
        landing_page_url: Landing page URL.

    Returns:
        Dict with 'success', 'message_id', and optionally 'error'.
    """
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone.replace("+", ""),
        "type": "interactive",
        "interactive": {
            "type": "cta_url",
            "header": {
                "type": "text",
                "text": "Quick Reminder 🔔",
            },
            "body": {
                "text": (
                    f"Hi {client_name},\n\n"
                    f"Just a friendly reminder — your review is ready to post!\n\n"
                    f"It only takes 30 seconds. Your feedback helps other "
                    f"businesses find the right partner. 🙏"
                ),
            },
            "action": {
                "name": "cta_url",
                "parameters": {
                    "display_text": "📋 Post Now",
                    "url": landing_page_url,
                },
            },
        },
    }

    return await _send_whatsapp_message(payload)


def verify_webhook(mode: str, token: str, challenge: str) -> str | None:
    """
    Verify Meta webhook subscription (GET request verification).

    Args:
        mode: Hub mode from query params (should be 'subscribe').
        token: Verification token from query params.
        challenge: Challenge string to echo back.

    Returns:
        Challenge string if verified, None otherwise.
    """
    settings = get_settings()

    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("WhatsApp webhook verified successfully")
        return challenge

    logger.warning(f"WhatsApp webhook verification failed: mode={mode}")
    return None


# ─── Internal Helper ──────────────────────────────────────


async def _send_whatsapp_message(payload: dict) -> dict:
    """
    Send a message via the WhatsApp Cloud API.

    Args:
        payload: Complete message payload dict.

    Returns:
        Dict with 'success' bool, 'message_id' str, and optional 'error'.
    """
    settings = get_settings()

    if not settings.WHATSAPP_ACCESS_TOKEN:
        logger.warning("WhatsApp not configured — skipping message")
        return {"success": False, "error": "WhatsApp not configured"}

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.whatsapp_api_url,
                json=payload,
                headers=headers,
            )

            result = response.json()

            if response.status_code != 200 or "error" in result:
                error_msg = result.get("error", {}).get("message", "Unknown error")
                logger.error(f"WhatsApp API error: {error_msg}")
                return {"success": False, "error": error_msg}

            message_id = result.get("messages", [{}])[0].get("id", "")
            logger.info(f"WhatsApp message sent: {message_id}")
            return {"success": True, "message_id": message_id}

    except httpx.TimeoutException:
        logger.error("WhatsApp API timeout")
        return {"success": False, "error": "Request timeout"}
    except Exception as e:
        logger.error(f"WhatsApp API exception: {e}")
        return {"success": False, "error": str(e)}


def _truncate(text: str, max_length: int) -> str:
    """Truncate text to max_length, adding ellipsis if truncated."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
