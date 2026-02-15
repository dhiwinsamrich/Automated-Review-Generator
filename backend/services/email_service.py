"""
Email service for fallback notifications and internal alerts.

Uses aiosmtplib for async SMTP email delivery.
"""

import html as html_lib

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from backend.config import get_settings
from backend.utils.logger import logger


def _esc(value: str) -> str:
    """Escape a string for safe insertion into HTML email templates."""
    return html_lib.escape(str(value)) if value else ""


async def send_consent_email(
    to_email: str,
    client_name: str,
    draft_text: str,
    landing_page_url: str,
) -> bool:
    """
    Send the review consent email (fallback when WhatsApp unavailable).

    Includes the draft text and a CTA button linking to the landing page.

    Args:
        to_email: Client's email address.
        client_name: Client's name for personalization.
        draft_text: AI-generated review draft.
        landing_page_url: URL to the copy+redirect landing page.

    Returns:
        True if email sent successfully, False otherwise.
    """
    settings = get_settings()

    subject = "Your Review Draft for bdcode — Quick Action Needed"

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
                    padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">bdcode</h1>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e9ecef;">
            <h2 style="color: #1F4E79; margin-top: 0;">Hi {client_name},</h2>

            <p style="color: #333; line-height: 1.6;">
                Thank you for your feedback on our recent project! Based on your
                responses, we've drafted a review for you:
            </p>

            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;
                        border-left: 4px solid #1F4E79; margin: 20px 0;">
                <p style="font-style: italic; margin: 0; color: #333; line-height: 1.6;">
                    "{draft_text}"
                </p>
            </div>

            <p style="color: #333; line-height: 1.6;">
                Click the button below to copy and post this review on Google:
            </p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{landing_page_url}"
                   style="display: inline-block; background: #4285F4; color: white;
                          padding: 14px 32px; text-decoration: none; border-radius: 8px;
                          font-weight: 600; font-size: 16px;">
                    📋 Copy & Post Review
                </a>
            </div>
        </div>

        <div style="background: #f8f9fa; padding: 20px; border-radius: 0 0 12px 12px;
                    text-align: center; border: 1px solid #e9ecef; border-top: none;">
            <p style="color: #999; margin: 0; font-size: 12px;">
                bdcode — Thank you for your partnership
            </p>
        </div>
    </div>
    """

    plain_text = (
        f"Hi {client_name},\n\n"
        f"Your review draft is ready: {landing_page_url}\n\n"
        f'Draft: "{draft_text}"\n\n'
        f"— bdcode Team"
    )

    return await _send_email(to_email, subject, html_body, plain_text)


async def send_internal_alert(
    client_name: str,
    company: str,
    avg_rating: float,
    open_feedback: str = "",
) -> bool:
    """
    Send an internal alert email for low-rated submissions.

    Sent to the configured ALERT_EMAILS recipients.

    Args:
        client_name: Client's name.
        company: Client's company.
        avg_rating: Average rating score.
        open_feedback: Optional Q10 open-text feedback.

    Returns:
        True if alert sent successfully.
    """
    settings = get_settings()
    recipients = settings.alert_email_list

    if not recipients:
        logger.warning("No ALERT_EMAILS configured — skipping internal alert")
        return False

    subject = f"[ACTION REQUIRED] Low Feedback Score from {client_name}"

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #DC3545; padding: 20px; border-radius: 12px 12px 0 0;">
            <h2 style="color: white; margin: 0;">⚠️ Low Feedback Alert</h2>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e9ecef;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; color: #666; width: 140px;"><strong>Client:</strong></td>
                    <td style="padding: 8px 0; color: #333;">{client_name}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;"><strong>Company:</strong></td>
                    <td style="padding: 8px 0; color: #333;">{company or 'N/A'}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;"><strong>Average Rating:</strong></td>
                    <td style="padding: 8px 0;">
                        <span style="background: #DC3545; color: white; padding: 4px 12px;
                                     border-radius: 4px; font-weight: 600;">
                            {avg_rating:.1f} / 10
                        </span>
                    </td>
                </tr>
            </table>

            {"<hr style='margin: 20px 0; border: none; border-top: 1px solid #eee;'>"
             "<p style='color: #666;'><strong>Client Feedback:</strong></p>"
             f"<p style='color: #333; line-height: 1.6;'>{open_feedback}</p>"
             if open_feedback else ""}

            <div style="background: #FFF3CD; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <p style="margin: 0; color: #856404;">
                    <strong>Recommended Action:</strong> Reach out to this client
                    to understand their concerns and address any issues.
                </p>
            </div>
        </div>
    </div>
    """

    # Send to all alert recipients
    success = True
    for recipient in recipients:
        result = await _send_email(recipient, subject, html_body)
        if not result:
            success = False

    return success


# ─── Internal Helper ──────────────────────────────────────


async def _send_email(
    to_email: str,
    subject: str,
    html_body: str,
    plain_text: str = "",
) -> bool:
    """
    Send an email via SMTP.

    Args:
        to_email: Recipient email address.
        subject: Email subject line.
        html_body: HTML content of the email.
        plain_text: Optional plain-text fallback.

    Returns:
        True if email sent successfully, False otherwise.
    """
    settings = get_settings()

    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured — skipping email")
        return False

    try:
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = to_email
        message["Subject"] = subject

        if plain_text:
            message.attach(MIMEText(plain_text, "plain"))
        message.attach(MIMEText(html_body, "html"))

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )

        logger.info(f"Email sent to {to_email}: {subject}")
        return True

    except Exception as e:
        logger.error(f"Email send failed to {to_email}: {e}")
        return False
