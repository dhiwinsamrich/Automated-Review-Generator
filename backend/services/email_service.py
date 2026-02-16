"""
Email service for fallback notifications and internal alerts.

Uses aiosmtplib for async SMTP email delivery.
"""

import html as html_lib
import uuid
from email.utils import formataddr, formatdate

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
    approve_url: str,
    regenerate_url: str,
    decline_url: str,
) -> bool:
    """
    Send the review consent email (fallback when WhatsApp unavailable).

    Includes the draft text and Approve / Regenerate / Decline buttons.

    Args:
        to_email: Client's email address.
        client_name: Client's name for personalization.
        draft_text: AI-generated review draft.
        approve_url: URL to approve the review.
        regenerate_url: URL to request a new draft.
        decline_url: URL to decline the review.

    Returns:
        True if email sent successfully, False otherwise.
    """
    safe_name = _esc(client_name)
    safe_draft = _esc(draft_text)

    subject = "Your Review Draft from bdcode is Ready"

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
                    padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">bdcode</h1>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e9ecef;">
            <h2 style="color: #1F4E79; margin-top: 0;">Hi {safe_name},</h2>

            <p style="color: #333; line-height: 1.6;">
                Thank you for your feedback on our recent project! Based on your
                responses, we've drafted a review for you:
            </p>

            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;
                        border-left: 4px solid #1F4E79; margin: 20px 0;">
                <p style="font-style: italic; margin: 0; color: #333; line-height: 1.6;">
                    "{safe_draft}"
                </p>
            </div>

            <p style="color: #333; line-height: 1.6;">
                Would you like to use this review? Choose an option below:
            </p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{approve_url}"
                   style="display: inline-block; background: #28A745; color: white;
                          padding: 14px 28px; text-decoration: none; border-radius: 8px;
                          font-weight: 600; font-size: 15px; margin: 6px;">
                    Approve
                </a>
                <a href="{regenerate_url}"
                   style="display: inline-block; background: #4285F4; color: white;
                          padding: 14px 28px; text-decoration: none; border-radius: 8px;
                          font-weight: 600; font-size: 15px; margin: 6px;">
                    Regenerate
                </a>
                <a href="{decline_url}"
                   style="display: inline-block; background: #6C757D; color: white;
                          padding: 14px 28px; text-decoration: none; border-radius: 8px;
                          font-weight: 600; font-size: 15px; margin: 6px;">
                    Decline
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
        f"We've drafted a review based on your feedback:\n\n"
        f'"{draft_text}"\n\n'
        f"Approve: {approve_url}\n"
        f"Regenerate: {regenerate_url}\n"
        f"Decline: {decline_url}\n\n"
        f"— bdcode Team"
    )

    return await _send_email(to_email, subject, html_body, plain_text)


async def send_approval_email(
    to_email: str,
    client_name: str,
    landing_page_url: str,
) -> bool:
    """
    Send the approval confirmation email with a link to copy & post the review.

    Sent after the client clicks Approve in the consent email.

    Args:
        to_email: Client's email address.
        client_name: Client's name.
        landing_page_url: URL to the landing page where they can copy the review.

    Returns:
        True if email sent successfully.
    """
    safe_name = _esc(client_name)

    subject = "Your Review is Approved — Post It Now!"

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
                    padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">bdcode</h1>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e9ecef;">
            <h2 style="color: #1F4E79; margin-top: 0;">Hi {safe_name},</h2>

            <p style="color: #333; line-height: 1.6;">
                Thank you for approving the review! Click the button below to copy
                the review text and post it on Google:
            </p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{landing_page_url}"
                   style="display: inline-block; background: #28A745; color: white;
                          padding: 14px 32px; text-decoration: none; border-radius: 8px;
                          font-weight: 600; font-size: 16px;">
                    Copy & Post Review
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
        f"Thank you for approving the review!\n\n"
        f"Copy & post it here: {landing_page_url}\n\n"
        f"— bdcode Team"
    )

    return await _send_email(to_email, subject, html_body, plain_text)


async def send_regenerated_email(
    to_email: str,
    client_name: str,
    draft_text: str,
    approve_url: str,
    regenerate_url: str | None,
    decline_url: str,
    regen_count: int,
) -> bool:
    """
    Send a new draft email after regeneration.

    If regen limit is reached, the Regenerate button is hidden.

    Args:
        to_email: Client's email address.
        client_name: Client's name.
        draft_text: New AI-generated review draft.
        approve_url: URL to approve.
        regenerate_url: URL to regenerate again (None if limit reached).
        decline_url: URL to decline.
        regen_count: Current regeneration count.

    Returns:
        True if email sent successfully.
    """
    settings = get_settings()
    safe_name = _esc(client_name)
    safe_draft = _esc(draft_text)
    is_final = regen_count >= settings.MAX_REGENERATIONS

    subject = "Your New Review Draft from bdcode"

    # Build regenerate button only if not at limit
    regenerate_button = ""
    regenerate_plain = ""
    if not is_final and regenerate_url:
        regenerate_button = f"""
                <a href="{regenerate_url}"
                   style="display: inline-block; background: #4285F4; color: white;
                          padding: 14px 28px; text-decoration: none; border-radius: 8px;
                          font-weight: 600; font-size: 15px; margin: 6px;">
                    Regenerate
                </a>"""
        regenerate_plain = f"Regenerate: {regenerate_url}\n"

    final_notice = ""
    if is_final:
        final_notice = """
            <p style="color: #856404; background: #FFF3CD; padding: 12px; border-radius: 6px;
                      font-size: 14px; text-align: center;">
                This is your final revision. Please approve or decline this draft.
            </p>"""

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
                    padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">bdcode</h1>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e9ecef;">
            <h2 style="color: #1F4E79; margin-top: 0;">Hi {safe_name},</h2>

            <p style="color: #333; line-height: 1.6;">
                Here's a new version of your review draft (revision {regen_count}):
            </p>

            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;
                        border-left: 4px solid #1F4E79; margin: 20px 0;">
                <p style="font-style: italic; margin: 0; color: #333; line-height: 1.6;">
                    "{safe_draft}"
                </p>
            </div>

            {final_notice}

            <p style="color: #333; line-height: 1.6;">
                Choose an option below:
            </p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{approve_url}"
                   style="display: inline-block; background: #28A745; color: white;
                          padding: 14px 28px; text-decoration: none; border-radius: 8px;
                          font-weight: 600; font-size: 15px; margin: 6px;">
                    Approve
                </a>{regenerate_button}
                <a href="{decline_url}"
                   style="display: inline-block; background: #6C757D; color: white;
                          padding: 14px 28px; text-decoration: none; border-radius: 8px;
                          font-weight: 600; font-size: 15px; margin: 6px;">
                    Decline
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

    final_plain = " (final revision)" if is_final else ""
    plain_text = (
        f"Hi {client_name},\n\n"
        f"Here's a new version of your review draft{final_plain}:\n\n"
        f'"{draft_text}"\n\n'
        f"Approve: {approve_url}\n"
        f"{regenerate_plain}"
        f"Decline: {decline_url}\n\n"
        f"— bdcode Team"
    )

    return await _send_email(to_email, subject, html_body, plain_text)


async def send_decline_email(
    to_email: str,
    client_name: str,
) -> bool:
    """
    Send a thank-you email after the client declines the review.

    Args:
        to_email: Client's email address.
        client_name: Client's name.

    Returns:
        True if email sent successfully.
    """
    safe_name = _esc(client_name)

    subject = "Thank You for Your Feedback — bdcode"

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
                    padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">bdcode</h1>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e9ecef;">
            <h2 style="color: #1F4E79; margin-top: 0;">Hi {safe_name},</h2>

            <p style="color: #333; line-height: 1.6;">
                Thank you for your time and for sharing your feedback with us.
                We truly appreciate your partnership and value your input.
            </p>

            <p style="color: #333; line-height: 1.6;">
                If you change your mind or have any questions, feel free to reach out
                to us anytime.
            </p>
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
        f"Thank you for your time and for sharing your feedback with us.\n"
        f"We truly appreciate your partnership.\n\n"
        f"— bdcode Team"
    )

    return await _send_email(to_email, subject, html_body, plain_text)


async def send_internal_alert(
    client_name: str,
    company: str,
    avg_rating: float,
    open_feedback: str = "",
    reason: str = "low_rating",
) -> bool:
    """
    Send an internal alert email for low-rated or consent-declined submissions.

    Sent to the configured ALERT_EMAILS recipients.

    Args:
        client_name: Client's name.
        company: Client's company.
        avg_rating: Average rating score.
        open_feedback: Optional Q10 open-text feedback.
        reason: Alert reason — 'low_rating' or 'consent_declined'.

    Returns:
        True if alert sent successfully.
    """
    settings = get_settings()
    recipients = settings.alert_email_list

    if not recipients:
        logger.warning("No ALERT_EMAILS configured — skipping internal alert")
        return False

    safe_name = _esc(client_name)
    safe_company = _esc(company) or "N/A"
    safe_feedback = _esc(open_feedback)

    if reason == "consent_declined":
        subject = f"[INFO] Testimonial Consent Declined by {client_name}"
        banner_color = "#FF8C00"
        banner_title = "Testimonial Consent Declined"
        action_text = (
            "This client gave a high satisfaction rating but declined "
            "testimonial consent. Consider a personal follow-up."
        )
    else:
        subject = f"[ACTION REQUIRED] Low Feedback Score from {client_name}"
        banner_color = "#DC3545"
        banner_title = "Low Feedback Alert"
        action_text = (
            "Reach out to this client to understand their concerns "
            "and address any issues."
        )

    rating_color = "#DC3545" if avg_rating < 8.0 else "#28A745"

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: {banner_color}; padding: 20px; border-radius: 12px 12px 0 0;">
            <h2 style="color: white; margin: 0;">{banner_title}</h2>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e9ecef;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; color: #666; width: 140px;"><strong>Client:</strong></td>
                    <td style="padding: 8px 0; color: #333;">{safe_name}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;"><strong>Company:</strong></td>
                    <td style="padding: 8px 0; color: #333;">{safe_company}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;"><strong>Average Rating:</strong></td>
                    <td style="padding: 8px 0;">
                        <span style="background: {rating_color}; color: white; padding: 4px 12px;
                                     border-radius: 4px; font-weight: 600;">
                            {avg_rating:.1f} / 10
                        </span>
                    </td>
                </tr>
            </table>

            {"<hr style='margin: 20px 0; border: none; border-top: 1px solid #eee;'>"
             "<p style='color: #666;'><strong>Client Feedback:</strong></p>"
             f"<p style='color: #333; line-height: 1.6;'>{safe_feedback}</p>"
             if safe_feedback else ""}

            <div style="background: #FFF3CD; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <p style="margin: 0; color: #856404;">
                    <strong>Recommended Action:</strong> {action_text}
                </p>
            </div>
        </div>
    </div>
    """

    plain_text = (
        f"{banner_title}\n\n"
        f"Client: {client_name}\n"
        f"Company: {company or 'N/A'}\n"
        f"Average Rating: {avg_rating:.1f}/10\n"
        f"{f'Feedback: {open_feedback}' if open_feedback else ''}\n\n"
        f"Action: {action_text}\n"
    )

    # Send to all alert recipients
    success = True
    for recipient in recipients:
        result = await _send_email(recipient, subject, html_body, plain_text)
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

        # Core headers
        message["From"] = formataddr((settings.SMTP_FROM_NAME, settings.SMTP_FROM_EMAIL))
        message["To"] = to_email
        message["Subject"] = subject
        message["Reply-To"] = settings.SMTP_FROM_EMAIL
        message["Date"] = formatdate(localtime=True)
        message["Message-ID"] = f"<{uuid.uuid4()}@{settings.SMTP_FROM_EMAIL.split('@')[-1]}>"

        # Anti-spam headers
        message["MIME-Version"] = "1.0"
        message["X-Mailer"] = "bdcode Review Generator"
        message["Precedence"] = "bulk"

        # Plain text MUST come first (spam filters check for it)
        if plain_text:
            message.attach(MIMEText(plain_text, "plain", "utf-8"))
        else:
            # Always include a plain-text version
            message.attach(MIMEText("Please view this email in an HTML-compatible client.", "plain", "utf-8"))
        message.attach(MIMEText(html_body, "html", "utf-8"))

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
