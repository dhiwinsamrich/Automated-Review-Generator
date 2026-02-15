"""
FastAPI application entrypoint.

Registers all routers and configures CORS for the React frontend.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routers import form_webhook, whatsapp_webhook, review
from backend.utils.logger import logger


# ─── Lifespan ────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    settings = get_settings()

    logger.info("=" * 60)
    logger.info("Automated Review Generator — Starting up")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Base URL: {settings.APP_BASE_URL}")
    logger.info(f"Frontend URL: {settings.FRONTEND_URL}")
    logger.info(f"Rating threshold: {settings.RATING_THRESHOLD}")
    logger.info(f"Token expiry: {settings.CONSENT_TOKEN_EXPIRY_DAYS} days")
    logger.info(f"Gemini API: {'configured' if settings.GEMINI_API_KEY else 'missing'}")
    logger.info(f"WhatsApp API: {'configured' if settings.WHATSAPP_ACCESS_TOKEN else 'missing'}")
    logger.info(f"SMTP: {'configured' if settings.SMTP_USERNAME else 'missing'}")
    logger.info(f"CRM Sheet: {'configured' if settings.CRM_SHEET_ID else 'missing'}")
    logger.info(f"GBP URL: {'configured' if settings.GBP_REVIEW_URL else 'missing'}")
    logger.info(f"Webhook secret: {'configured' if settings.WEBHOOK_SECRET else 'NOT SET (insecure)'}")
    logger.info("=" * 60)

    yield

    logger.info("Automated Review Generator — Shutting down")


# ─── App Initialization ──────────────────────────────────

app = FastAPI(
    title="Automated Review Generator",
    description=(
        "Automated system that collects client feedback, qualifies responses, "
        "generates AI review drafts, and facilitates posting on Google Business Profile."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ─── CORS Middleware ──────────────────────────────────────

settings = get_settings()

# In production, only allow the configured frontend URL
# In development, also allow common localhost origins
allowed_origins = [settings.FRONTEND_URL]
if settings.ENVIRONMENT == "development":
    allowed_origins.extend([
        "http://localhost:5173",
        "http://localhost:3000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Router Registration ─────────────────────────────────

app.include_router(form_webhook.router)
app.include_router(whatsapp_webhook.router)
app.include_router(review.router)


# ─── Health Check ─────────────────────────────────────────


@app.get("/health", tags=["System"])
async def health_check():
    """Health check with dependency status."""
    settings = get_settings()

    return {
        "status": "healthy",
        "service": "Automated Review Generator",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "dependencies": {
            "gemini_api": "configured" if settings.GEMINI_API_KEY else "missing",
            "google_sheets": "configured" if settings.FORM_RESPONSES_SHEET_ID else "missing",
            "crm_sheet": "configured" if settings.CRM_SHEET_ID else "missing",
            "whatsapp": "configured" if settings.WHATSAPP_ACCESS_TOKEN else "missing",
            "smtp": "configured" if settings.SMTP_USERNAME else "missing",
            "gbp_url": "configured" if settings.GBP_REVIEW_URL else "missing",
            "webhook_secret": "configured" if settings.WEBHOOK_SECRET else "NOT SET",
        },
    }


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Automated Review Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "form_webhook": "POST /api/webhook/form",
            "whatsapp_webhook": "GET/POST /api/webhook/whatsapp",
            "review": "GET /api/review/{token}",
            "health": "GET /health",
        },
    }
