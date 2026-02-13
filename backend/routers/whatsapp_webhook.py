"""
WhatsApp webhook router.

Handles two responsibilities:
1. GET /api/webhook/whatsapp — Meta webhook verification
2. POST /api/webhook/whatsapp — Incoming messages (Approve/Edit/Decline)
"""

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from backend.config import get_settings
from backend.models.schemas import SubmissionStatus, WebhookResponse
from backend.services import whatsapp_service, sheets_service, notification_service
from backend.models.schemas import ClientData
from backend.utils.logger import logger

router = APIRouter(prefix="/api/webhook", tags=["Webhooks"])


@router.get("/whatsapp")
async def verify_whatsapp_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """
    Handle Meta webhook verification (GET request).

    Meta sends this when you configure the webhook URL in the
    WhatsApp Business API settings. Must echo back the challenge.
    """
    if not hub_mode or not hub_token or not hub_challenge:
        raise HTTPException(status_code=400, detail="Missing verification parameters")

    challenge = whatsapp_service.verify_webhook(hub_mode, hub_token, hub_challenge)

    if challenge:
        return PlainTextResponse(content=challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def handle_whatsapp_message(request: Request):
    """
    Handle incoming WhatsApp messages and button responses.

    Parses the webhook payload from Meta to extract the client's
    response (Approve/Edit/Decline) and routes accordingly.
    """
    settings = get_settings()
    sheet_id = settings.FORM_RESPONSES_SHEET_ID

    try:
        body = await request.json()
    except Exception:
        return WebhookResponse(success=False, message="Invalid JSON payload")

    # Meta sends a complex nested structure — extract the message
    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            # Not a message event (could be status update) — acknowledge
            return WebhookResponse(success=True, message="No message to process")

        message = messages[0]
        from_number = message.get("from", "")
        message_type = message.get("type", "")

        # Handle interactive button replies (Approve/Edit/Decline)
        if message_type == "interactive":
            interactive = message.get("interactive", {})
            button_reply = interactive.get("button_reply", {})
            button_id = button_reply.get("id", "")

            logger.info(f"WhatsApp button reply from {from_number}: {button_id}")

            # Parse action and token from button ID (format: "action_token")
            if "_" in button_id:
                parts = button_id.split("_", 1)
                action = parts[0]
                token = parts[1]

                return await _handle_consent_response(
                    sheet_id=sheet_id,
                    action=action,
                    token=token,
                    from_number=from_number,
                )

        # Handle text messages (free-form replies)
        elif message_type == "text":
            text = message.get("text", {}).get("body", "").strip().lower()
            logger.info(f"WhatsApp text from {from_number}: {text}")
            # For now, just acknowledge text messages
            return WebhookResponse(
                success=True,
                message="Text message received. Please use the buttons to respond.",
            )

        return WebhookResponse(success=True, message="Message processed")

    except Exception as e:
        logger.error(f"WhatsApp webhook processing error: {e}")
        # Always return 200 to Meta to avoid webhook retry floods
        return WebhookResponse(success=False, message=str(e))


async def _handle_consent_response(
    sheet_id: str,
    action: str,
    token: str,
    from_number: str,
) -> WebhookResponse:
    """
    Handle a consent action (approve/edit/decline) from WhatsApp.

    Args:
        sheet_id: Form responses sheet ID.
        action: One of 'approve', 'edit', 'decline'.
        token: Consent token identifying the submission.
        from_number: Client's WhatsApp number.

    Returns:
        WebhookResponse with result.
    """
    # Look up the submission by token
    review_data = sheets_service.get_review_by_token(sheet_id, token)

    if not review_data:
        logger.warning(f"Token not found: {token}")
        return WebhookResponse(
            success=False,
            message="Invalid or expired token",
        )

    row = review_data["row"]
    client_name = review_data.get("client_name", "Valued Client")

    if action == "approve":
        logger.info(f"Review APPROVED for row {row} by {from_number}")

        # Update status
        sheets_service.update_submission_row(sheet_id, row, {
            "status": SubmissionStatus.APPROVED.value,
        })

        # Build client data for notification
        client_data = ClientData(
            name=client_name,
            company=review_data.get("company", ""),
            whatsapp=f"+{from_number}" if not from_number.startswith("+") else from_number,
        )

        # Send Message 2 (landing page URL)
        result = await notification_service.send_approval_notification(
            client_data=client_data,
            token=token,
        )

        sheets_service.log_audit_event(
            sheet_id, "APPROVED", f"row_{row}",
            f"Client approved via WhatsApp. Landing page link sent via {result.method.value}."
        )

        return WebhookResponse(
            success=True,
            message=f"Review approved. Landing page link sent to {client_name}.",
            data={"action": "approve", "row": row},
        )

    elif action == "edit":
        logger.info(f"Review EDIT requested for row {row} by {from_number}")

        sheets_service.update_submission_row(sheet_id, row, {
            "status": SubmissionStatus.EDITED.value,
        })

        sheets_service.log_audit_event(
            sheet_id, "EDIT_REQUESTED", f"row_{row}",
            "Client requested edit via WhatsApp."
        )

        # TODO Phase 2: Implement edit flow (regenerate or collect edits)
        return WebhookResponse(
            success=True,
            message="Edit request received. We'll send you an updated draft soon.",
            data={"action": "edit", "row": row},
        )

    elif action == "decline":
        logger.info(f"Review DECLINED for row {row} by {from_number}")

        sheets_service.update_submission_row(sheet_id, row, {
            "status": SubmissionStatus.DECLINED.value,
        })

        sheets_service.log_audit_event(
            sheet_id, "DECLINED", f"row_{row}",
            "Client declined via WhatsApp. No further messages."
        )

        return WebhookResponse(
            success=True,
            message="Review declined. No further messages will be sent.",
            data={"action": "decline", "row": row},
        )

    else:
        logger.warning(f"Unknown action: {action}")
        return WebhookResponse(
            success=False,
            message=f"Unknown action: {action}",
        )
