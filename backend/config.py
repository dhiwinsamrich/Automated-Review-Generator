"""
Application configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """All application settings, loaded from .env file."""

    # --- Gemini AI ---
    GEMINI_API_KEY: str = ""

    # --- Google Business Profile ---
    GBP_REVIEW_URL: str = ""

    # --- Google Sheets ---
    FORM_RESPONSES_SHEET_ID: str = ""
    CRM_SHEET_ID: str = ""
    GOOGLE_SERVICE_ACCOUNT_FILE: str = "service_account.json"

    # --- WhatsApp Business API ---
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_VERIFY_TOKEN: str = ""
    WHATSAPP_API_VERSION: str = "v18.0"
    WHATSAPP_TEMPLATE_NAME: str = "review_consent"  # Message 1: consent request
    WHATSAPP_TEMPLATE_NAME_APPROVED: str = "review_approved"  # Message 2: approved with URL button
    WHATSAPP_TEMPLATE_LANGUAGE: str = "en"

    # --- Email (SMTP Fallback) ---
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "bdcode Team"

    # --- Internal Alerts ---
    ALERT_EMAILS: str = ""  # comma-separated

    # --- Qualification ---
    RATING_THRESHOLD: float = 8.0

    # --- Email Regeneration ---
    MAX_REGENERATIONS: int = 2

    # --- Application ---
    APP_BASE_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:8080"
    # FRONTEND_URL: str = "https://automated-review-generator.vercel.app"

    # --- Webhook Security ---
    WEBHOOK_SECRET: str = ""

    # --- Token Expiry ---
    CONSENT_TOKEN_EXPIRY_DAYS: int = 14

    # --- Phone Number ---
    DEFAULT_COUNTRY_CODE: str = "+91"

    # --- Environment ---
    ENVIRONMENT: str = "development"  # development | production

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @property
    def alert_email_list(self) -> list[str]:
        """Parse comma-separated alert emails into a list."""
        if not self.ALERT_EMAILS:
            return []
        return [e.strip() for e in self.ALERT_EMAILS.split(",") if e.strip()]

    @property
    def whatsapp_api_url(self) -> str:
        """Construct the WhatsApp API base URL."""
        return (
            f"https://graph.facebook.com/{self.WHATSAPP_API_VERSION}"
            f"/{self.WHATSAPP_PHONE_NUMBER_ID}/messages"
        )


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance — loaded once at startup."""
    return Settings()
