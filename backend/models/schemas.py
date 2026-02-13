"""
Pydantic models for request/response data throughout the application.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


# ─── Enums ────────────────────────────────────────────────

class ConsentAction(str, Enum):
    APPROVE = "approve"
    EDIT = "edit"
    DECLINE = "decline"


class SubmissionStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    APPROVED = "APPROVED"
    EDITED = "EDITED"
    DECLINED = "DECLINED"
    COPIED = "COPIED"
    POSTED = "POSTED"
    ALERT_SENT = "ALERT_SENT"


class DeliveryMethod(str, Enum):
    WHATSAPP = "WHATSAPP"
    EMAIL = "EMAIL"
    NONE = "NONE"


# ─── Form Submission ─────────────────────────────────────

class FormSubmissionData(BaseModel):
    """Data received from Google Apps Script webhook on form submission."""

    row_number: int
    timestamp: str
    email: str

    # LinkedIn profile (optional)
    linkedin_profile: Optional[str] = None

    # Q1-Q8 ratings (1-10 scale)
    q1_kickoff_satisfaction: Optional[float] = None
    q2_communication: Optional[float] = None
    q3_project_management: Optional[float] = None
    q4_design_ux: Optional[float] = None
    q5_technical_quality: Optional[float] = None
    q6_launch_smoothness: Optional[float] = None
    q7_support_handover: Optional[float] = None
    q8_overall_satisfaction: Optional[float] = None

    # Q9 consent
    q9_testimonial_consent: str = "No"

    # Q10 open text
    q10_open_feedback: Optional[str] = None

    # Source sheet ID
    sheet_id: Optional[str] = None

    @property
    def ratings(self) -> list[Optional[float]]:
        """Return all Q1-Q8 rating values as a list."""
        return [
            self.q1_kickoff_satisfaction,
            self.q2_communication,
            self.q3_project_management,
            self.q4_design_ux,
            self.q5_technical_quality,
            self.q6_launch_smoothness,
            self.q7_support_handover,
            self.q8_overall_satisfaction,
        ]

    @property
    def ratings_breakdown(self) -> dict:
        """Return ratings as a labeled dictionary for prompt building."""
        return {
            "q1": self.q1_kickoff_satisfaction,
            "q2": self.q2_communication,
            "q3": self.q3_project_management,
            "q4": self.q4_design_ux,
            "q5": self.q5_technical_quality,
            "q6": self.q6_launch_smoothness,
            "q7": self.q7_support_handover,
            "q8": self.q8_overall_satisfaction,
        }


# ─── Client Data (CRM Lookup) ────────────────────────────

class ClientData(BaseModel):
    """Client information retrieved from the internal CRM Google Sheet."""

    name: str = "Valued Client"
    company: str = ""
    services: str = ""
    whatsapp: Optional[str] = None
    business_email: str = ""
    found: bool = False


# ─── Qualification ────────────────────────────────────────

class QualificationResult(BaseModel):
    """Result of the rating qualification check."""

    avg_rating: float
    is_qualified: bool
    consent_given: bool


# ─── Review ───────────────────────────────────────────────

class ReviewDraft(BaseModel):
    """Generated review draft with metadata."""

    draft_text: str
    token: str
    client_name: str
    company: str = ""
    created_at: datetime


class ReviewResponse(BaseModel):
    """Response payload for the landing page API (GET /api/review/{token})."""

    draft_text: str
    client_name: str
    gbp_review_url: str
    status: str


# ─── Notification ─────────────────────────────────────────

class NotificationResult(BaseModel):
    """Result of sending a notification (WhatsApp or email)."""

    method: DeliveryMethod
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None


# ─── Webhook Payloads ─────────────────────────────────────

class WebhookResponse(BaseModel):
    """Standard webhook response."""

    success: bool
    message: str
    data: Optional[dict] = None
