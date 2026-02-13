# Automated Review Generator

Automated system that collects client feedback via Google Forms, qualifies responses, generates AI review drafts using Gemini, and facilitates posting on Google Business Profile — via WhatsApp (primary) or email (fallback).

---

## Prerequisites

- **Python 3.11+** (via Conda)
- **Node.js 18+** (for the React frontend)
- **Google Cloud account** (for Sheets API service account)
- **Meta Business account** (for WhatsApp Business API — can set up later)

---

## 1. Environment Setup

### 1.1 Conda Environment

```bash
# Create the conda environment (one-time)
conda create -n review-generator python=3.11 -y

# Activate it
conda activate review-generator

# Install Python dependencies
cd "d:\@White Mastery Systems\Automated Review Generator"
pip install -r requirements.txt
```

### 1.2 Frontend Dependencies

```bash
cd frontend
npm install
```

### 1.3 Configure `.env`

Copy the example and fill in your values:

```bash
copy .env.example .env
```

Then edit `.env` with your credentials:

| Variable | Description | Required Now? |
|----------|-------------|:---:|
| `GEMINI_API_KEY` | Your Google Gemini API key | ✅ Yes |
| `GBP_REVIEW_URL` | Google Business Profile review URL (e.g. `https://g.page/r/YOUR_CID/review`) | Later |
| `FORM_RESPONSES_SHEET_ID` | Sheet ID from the Google Form responses URL | Later |
| `CRM_SHEET_ID` | Sheet ID of your internal client CRM | Later |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to your service account JSON key | Later |
| `WHATSAPP_ACCESS_TOKEN` | Meta WhatsApp Business API access token | Later |
| `WHATSAPP_PHONE_NUMBER_ID` | WhatsApp registered phone number ID | Later |
| `WHATSAPP_VERIFY_TOKEN` | Any random string for webhook verification | Later |
| `SMTP_USERNAME` | Gmail address for email fallback | Later |
| `SMTP_PASSWORD` | Gmail App Password (not your login password) | Later |
| `SMTP_FROM_EMAIL` | From address for outgoing emails | Later |
| `ALERT_EMAILS` | Comma-separated emails for low-rating alerts | Later |

> **Tip:** The app will start even with empty values — features just won't work until configured.

---

## 2. Google Cloud Service Account Setup

This is needed for the Google Sheets integration (CRM lookup + status tracking).

### Steps:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. **Enable APIs:**
   - Search for "Google Sheets API" → Enable
   - Search for "Google Drive API" → Enable
4. **Create Service Account:**
   - Go to IAM & Admin → Service Accounts
   - Click "Create Service Account"
   - Give it a name (e.g. `review-generator`)
   - Skip role assignment → Done
5. **Download JSON key:**
   - Click the service account → Keys tab
   - Add Key → Create new key → JSON → Download
   - Save the file as `service_account.json` in the project root
6. **Share your Google Sheets:**
   - Open the service account details and copy its email (looks like `name@project.iam.gserviceaccount.com`)
   - Open each Google Sheet (Form Responses + CRM) → Share → paste the service account email → Editor access

Then update `.env`:
```
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
FORM_RESPONSES_SHEET_ID=<your-form-sheet-id>
CRM_SHEET_ID=<your-crm-sheet-id>
```

> **Where to find Sheet ID:** Open the sheet → the ID is in the URL:
> `https://docs.google.com/spreadsheets/d/`**THIS_PART_IS_THE_ID**`/edit`

---

## 3. Install Google Apps Script Trigger

This fires when a client submits the feedback form.

1. Open your Google Sheet (linked to the feedback form)
2. Go to **Extensions → Apps Script**
3. Delete any existing code
4. Paste the contents of `scripts/google_apps_script.js`
5. Update `WEBHOOK_URL` at the top:
   - For local dev: use ngrok URL (see below)
   - For production: your server URL
6. Click **Run → `onFormSubmit`** (to authorize permissions)
7. Go to **Triggers** (clock icon) → **Add Trigger:**
   - Function: `onFormSubmit`
   - Event source: `From spreadsheet`
   - Event type: `On form submit`
8. Save

---

## 4. Running the Application

### Backend (Terminal 1)

```bash
conda activate review-generator
cd "d:\@White Mastery Systems\Automated Review Generator"
uvicorn backend.main:app --reload --port 8000
```

You should see:
```
INFO     | review_generator | ============================================================
INFO     | review_generator | Automated Review Generator — Starting up
INFO     | review_generator | Gemini API: ✅ configured
INFO     | Application startup complete.
```

### Frontend (Terminal 2)

```bash
cd "d:\@White Mastery Systems\Automated Review Generator\frontend"
npm run dev
```

Opens on `http://localhost:5173`

### API Docs

Open **http://localhost:8000/docs** in your browser — interactive Swagger UI to test all endpoints.

---

## 5. Local Development with ngrok

Since WhatsApp and Google Apps Script need to reach your local server, use ngrok:

```bash
# Install ngrok (one-time): https://ngrok.com/download
ngrok http 8000
```

This gives you a public URL like `https://xxxx.ngrok.io`. Use it for:
- `WEBHOOK_URL` in the Google Apps Script
- WhatsApp webhook URL in Meta Business settings
- `APP_BASE_URL` in your `.env`

---

## 6. Testing

### Quick Health Check
```bash
curl http://localhost:8000/health
```

### Test Form Submission (simulated)
```bash
curl -X POST http://localhost:8000/api/webhook/form ^
  -H "Content-Type: application/json" ^
  -d "{\"row_number\": 2, \"timestamp\": \"2026-02-13\", \"email\": \"test@example.com\", \"q1_kickoff_satisfaction\": 9, \"q2_communication\": 9, \"q3_project_management\": 8, \"q4_design_ux\": 9, \"q5_technical_quality\": 8, \"q6_launch_smoothness\": 9, \"q7_support_handover\": 8, \"q8_overall_satisfaction\": 9, \"q9_testimonial_consent\": \"Yes\", \"q10_open_feedback\": \"Great team!\"}"
```

### Test Landing Page
Open `http://localhost:5173/review/test-token-123` in your browser (will show error until there's real data).

---

## Project Structure

```
├── .env                          # Your config (gitignored)
├── .env.example                  # Config template
├── requirements.txt              # Python dependencies
├── service_account.json          # Google credentials (gitignored)
├── backend/
│   ├── main.py                   # FastAPI app
│   ├── config.py                 # Settings from .env
│   ├── models/schemas.py         # Data models
│   ├── prompts/
│   │   └── review_generation.py  # AI prompt templates
│   ├── services/                 # Business logic
│   └── routers/                  # API endpoints
├── frontend/                     # React landing page
└── scripts/
    └── google_apps_script.js     # Form trigger
```
