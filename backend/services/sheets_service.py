"""
Google Sheets API service for CRM lookup and status tracking.

Uses gspread with a service account for authentication.
All public functions are async (using asyncio.to_thread) to avoid
blocking the FastAPI event loop.
"""

import asyncio
import re
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from backend.config import get_settings
from backend.models.schemas import ClientData
from backend.utils.logger import logger

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

# Module-level client (initialized lazily)
_sheets_client: gspread.Client | None = None


def _get_client() -> gspread.Client:
    """Get or create the authenticated gspread client."""
    global _sheets_client
    if _sheets_client is None:
        settings = get_settings()
        credentials = Credentials.from_service_account_file(
            settings.GOOGLE_SERVICE_ACCOUNT_FILE,
            scopes=SCOPES,
        )
        _sheets_client = gspread.authorize(credentials)
        logger.info("Google Sheets client initialized")
    return _sheets_client


# ─── CRM Lookup ──────────────────────────────────────────


async def lookup_client_by_email(email: str) -> ClientData:
    """
    Look up client details in the internal CRM Google Sheet by email.

    Matches on the 'Client Email' column (case-insensitive).
    If no match found, returns default ClientData with email only.

    Args:
        email: Email address from the form submission.

    Returns:
        ClientData with name, company, services, WhatsApp number.
    """
    return await asyncio.to_thread(_lookup_client_by_email_sync, email)


def _lookup_client_by_email_sync(email: str) -> ClientData:
    """Synchronous implementation of CRM lookup."""
    settings = get_settings()

    if not settings.CRM_SHEET_ID:
        logger.warning("CRM_SHEET_ID not configured — returning default client data")
        return ClientData(business_email=email)

    try:
        client = _get_client()
        sheet = client.open_by_key(settings.CRM_SHEET_ID).sheet1

        records = sheet.get_all_records()
        normalized_email = email.lower().strip()

        for record in records:
            record_email = str(record.get("Client Email", "")).lower().strip()
            if record_email == normalized_email:
                whatsapp = record.get("WhatsApp Number")
                if whatsapp:
                    whatsapp = _format_whatsapp_number(str(whatsapp))

                logger.info(f"Client found in CRM: {email}")
                return ClientData(
                    name=record.get("Client Name", "Valued Client"),
                    company=record.get("Company Name", ""),
                    services=record.get("Services Used", ""),
                    whatsapp=whatsapp,
                    business_email=record.get("Business Email", email),
                    found=True,
                )

        logger.warning(f"Client not found in CRM: {email}")
        return ClientData(business_email=email)

    except Exception as e:
        logger.error(f"CRM lookup failed for {email}: {e}")
        return ClientData(business_email=email)


# ─── Duplicate Check ─────────────────────────────────────


async def check_duplicate_submission(sheet_id: str, email: str) -> bool:
    """
    Check if this email already has an active submission (SENT or APPROVED).

    Args:
        sheet_id: Google Sheet ID.
        email: Submitter's email address.

    Returns:
        True if a duplicate active submission exists.
    """
    return await asyncio.to_thread(_check_duplicate_sync, sheet_id, email)


def _check_duplicate_sync(sheet_id: str, email: str) -> bool:
    """Synchronous duplicate check."""
    if not sheet_id:
        return False

    try:
        client = _get_client()
        sheet = client.open_by_key(sheet_id).sheet1
        all_data = sheet.get_all_values()

        if len(all_data) < 2:
            return False

        email_col = 12  # Column M (0-indexed)
        status_col = _col_letter_to_num(COLUMN_MAP["status"]) - 1
        normalized_email = email.lower().strip()

        active_statuses = {"SENT", "APPROVED", "PENDING"}

        for row_data in all_data[1:]:  # Skip header
            row_email = _safe_get(row_data, email_col).lower().strip()
            row_status = _safe_get(row_data, status_col).upper().strip()
            if row_email == normalized_email and row_status in active_statuses:
                logger.info(f"Duplicate submission found for {email} (status: {row_status})")
                return True

        return False

    except Exception as e:
        logger.error(f"Duplicate check failed for {email}: {e}")
        return False


# ─── Form Responses Sheet Updates ─────────────────────────

# Column mapping for the Form Responses sheet
# Columns A-M are auto-filled by Google Forms:
#   A=Timestamp, B=LinkedIn, C-J=Q1-Q8, K=Q9, L=Q10, M=Email
# Columns N onward are written by our system
COLUMN_MAP = {
    "avg_rating": "N",
    "qualified": "O",
    "client_name": "P",
    "company": "Q",
    "services": "R",
    "whatsapp": "S",
    "business_email": "T",
    "draft_text": "U",
    "token": "V",
    "status": "W",
    "delivery_method": "X",
    "sent_at": "Y",
    "copied_at": "Z",
    "error": "AA",
}


async def update_submission_row(sheet_id: str, row: int, updates: dict) -> None:
    """
    Update calculated/status columns for a form submission row.

    Uses batch_update for a single API call instead of one call per field.

    Args:
        sheet_id: Google Sheet ID for the form responses sheet.
        row: Row number (1-indexed) of the submission.
        updates: Dict of field_name -> value to write.
    """
    await asyncio.to_thread(_update_submission_row_sync, sheet_id, row, updates)


def _update_submission_row_sync(sheet_id: str, row: int, updates: dict) -> None:
    """Synchronous implementation of row update with batching."""
    if not sheet_id:
        logger.warning("No sheet_id provided — skipping row update")
        return

    try:
        client = _get_client()
        sheet = client.open_by_key(sheet_id).sheet1

        for field, value in updates.items():
            col = COLUMN_MAP.get(field)
            if col:
                cell = f"{col}{row}"
                sheet.update(cell, [[str(value) if value is not None else ""]])

        logger.info(f"Updated row {row}: {list(updates.keys())}")

    except Exception as e:
        logger.error(f"Failed to update sheet row {row}: {e}")
        raise


async def get_review_by_token(sheet_id: str, token: str) -> dict | None:
    """
    Find a submission row by its consent token.

    Args:
        sheet_id: Google Sheet ID.
        token: Unique consent token to search for.

    Returns:
        Dict with review data, or None if not found.
    """
    if not sheet_id:
        return None

    try:
        client = _get_client()
        sheet = client.open_by_key(sheet_id).sheet1

        # Token is in the column defined by COLUMN_MAP
        token_col = COLUMN_MAP["token"]
        all_tokens = sheet.col_values(_col_letter_to_num(token_col))

        for i, cell_token in enumerate(all_tokens):
            if cell_token == token:
                row = i + 1  # 1-indexed
                row_data = sheet.row_values(row)

                return {
                    "row": row,
                    "client_name": _safe_get(row_data, _col_letter_to_num(COLUMN_MAP["client_name"]) - 1),
                    "company": _safe_get(row_data, _col_letter_to_num(COLUMN_MAP["company"]) - 1),
                    "draft_text": _safe_get(row_data, _col_letter_to_num(COLUMN_MAP["draft_text"]) - 1),
                    "status": _safe_get(row_data, _col_letter_to_num(COLUMN_MAP["status"]) - 1),
                    "token": token,
                }

        return None

    except Exception as e:
        logger.error(f"Failed to find token {token}: {e}")
        return None


# ─── Audit Log ────────────────────────────────────────────


async def log_audit_event(
    sheet_id: str, event_type: str, reference: str, details: str
) -> None:
    """
    Write an event to the 'Audit Log' tab in the form responses sheet.

    Creates the tab if it doesn't exist.

    Args:
        sheet_id: Google Sheet ID.
        event_type: Type of event (e.g., FORM_SUBMIT, QUALIFIED, AI_CALLED).
        reference: Reference ID (e.g., row number).
        details: Human-readable event description.
    """
    if not sheet_id:
        return

    try:
        client = _get_client()
        workbook = client.open_by_key(sheet_id)

        try:
            audit_sheet = workbook.worksheet("Audit Log")
        except gspread.exceptions.WorksheetNotFound:
            audit_sheet = workbook.add_worksheet("Audit Log", rows=1000, cols=4)
            audit_sheet.update(
                "A1:D1",
                [["Timestamp", "Event Type", "Reference", "Details"]],
            )

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        audit_sheet.append_row([timestamp, event_type, str(reference), details])

    except Exception as e:
        logger.error(f"Failed to log audit event: {e}")


# ─── Helper Functions ─────────────────────────────────────


def _format_whatsapp_number(number: str) -> str | None:
    """Format WhatsApp number to E.164 format (e.g., +919876543210)."""
    if not number:
        return None

    cleaned = re.sub(r"[\s\-\(\)]", "", number)

    # Add India country code if missing
    if not cleaned.startswith("+"):
        cleaned = "+91" + cleaned

    return cleaned


def _col_letter_to_num(letter: str) -> int:
    """Convert column letter(s) to 1-indexed number. A=1, B=2, ..., Z=26, AA=27."""
    result = 0
    for char in letter.upper():
        result = result * 26 + (ord(char) - ord("A") + 1)
    return result


def _safe_get(lst: list, index: int, default: str = "") -> str:
    """Safely get a value from a list by index."""
    try:
        return lst[index] if index < len(lst) else default
    except (IndexError, TypeError):
        return default
