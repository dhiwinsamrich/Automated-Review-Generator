# Setup Checklist — Automated Review Generator

Complete these steps in order to get the application fully operational.

---

## 1. Conda Environment + Dependencies

```bash
# Create environment (one-time)
conda create -n review-generator python=3.11 -y

# Activate
conda activate review-generator

# Install Python dependencies
cd "d:\@White Mastery Systems\Automated Review Generator"
pip install -r requirements.txt
```

```bash
# Install frontend dependencies
cd frontend
npm install
```

- [ ] Conda environment created and activated
- [ ] `pip install -r requirements.txt` completed
- [ ] `npm install` completed in `frontend/`

---

## 2. Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click **Create API Key**
3. Copy the key

**Update `.env`:**
```
GEMINI_API_KEY=your-actual-api-key
```

- [ ] Gemini API key generated
- [ ] Pasted into `.env`

---

## 3. Google Cloud Service Account (For Sheets API)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. **Enable APIs:**
   - Search "Google Sheets API" → Enable
   - Search "Google Drive API" → Enable
4. **Create Service Account:**
   - IAM & Admin → Service Accounts → Create Service Account
   - Name: `review-generator`
   - Skip role assignment → Done
5. **Download JSON key:**
   - Click the service account → Keys tab
   - Add Key → Create new key → JSON → Download
   - Save the file in the project root
6. **Copy the service account email** (looks like `name@project.iam.gserviceaccount.com`) — you'll need it for sharing sheets

**Update `.env`:**
```
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
```

> **Important:** Your `.env` currently has `GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json`.
> Make sure your downloaded file is named exactly that, or update the `.env` value to match
> your actual filename (e.g. `credentials.json`).

- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Google Drive API enabled
- [ ] Service account created
- [ ] JSON key downloaded and placed in project root
- [ ] Service account email copied (for sharing sheets later)
- [ ] `GOOGLE_SERVICE_ACCOUNT_FILE` set in `.env`

---

## 4. Google Form (Client Feedback Form)

Create a Google Form with these fields (matching `Client Feedback Form.pdf`):

| # | Question | Type | Scale |
|---|----------|------|-------|
| 0 | LinkedIn profile link | Short text | — |
| 1 | Kickoff process satisfaction | Linear scale | 1–10 |
| 2 | Communication quality | Linear scale | 1–10 |
| 3 | Project planning & management | Linear scale | 1–10 |
| 4 | Design, branding & UX | Linear scale | 1–10 |
| 5 | Technical quality & performance | Linear scale | 1–10 |
| 6 | Testing & launch smoothness | Linear scale | 1–10 |
| 7 | Training, handover & support | Linear scale | 1–10 |
| 8 | Overall satisfaction | Linear scale | 1–10 |
| 9 | May we use feedback as testimonial? | Multiple choice | Yes / No |
| 10 | Anything else to share? | Long text | — |

**Settings:**
- Under Settings → Responses → "Collect email addresses" → **Verified**
- Link responses to a Google Sheet (Responses tab → green Sheets icon)

- [ ] Google Form created with all 11 fields
- [ ] Email collection enabled (verified)
- [ ] Form linked to a Google Sheet

---

## 5. Form Responses Google Sheet

1. Open the Google Sheet linked to your form
2. Copy the **Sheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_IS_HERE/edit
   ```
3. **Share** the sheet with your service account email → **Editor** access

**Update `.env`:**
```
FORM_RESPONSES_SHEET_ID=your-form-responses-sheet-id
```

- [ ] Form Responses Sheet ID copied
- [ ] Sheet shared with service account email (Editor)
- [ ] `FORM_RESPONSES_SHEET_ID` set in `.env`

---

## 6. CRM Google Sheet (Internal Client Database)

Create a new Google Sheet with **exactly these column headers** in Row 1:

| Client Email | Client Name | Company Name | Services Used | WhatsApp Number | Business Email |
|---|---|---|---|---|---|
| john@acme.com | John Doe | Acme Corp | Web Development | +919876543210 | john@acme.com |

> The system looks up clients by matching the form submitter's email against the
> "Client Email" column (case-insensitive). Populate this sheet with your existing clients.

1. Copy the Sheet ID from the URL
2. **Share** with your service account email → **Editor** access

**Update `.env`:**
```
CRM_SHEET_ID=your-crm-sheet-id
```

- [ ] CRM Sheet created with correct column headers
- [ ] At least one test client row added
- [ ] Sheet shared with service account email (Editor)
- [ ] `CRM_SHEET_ID` set in `.env`

---

## 7. Google Business Profile Review URL

1. Search your business on [Google Maps](https://maps.google.com)
2. Click your business → "Write a review" → copy the URL
3. Or use [Google Place ID Finder](https://developers.google.com/maps/documentation/places/web-service/place-id) to find your Place ID, then construct:
   ```
   https://search.google.com/local/writereview?placeid=YOUR_PLACE_ID
   ```

**Update `.env`:**
```
GBP_REVIEW_URL=https://search.google.com/local/writereview?placeid=YOUR_PLACE_ID
```

- [ ] Google Business Profile review URL obtained
- [ ] `GBP_REVIEW_URL` set in `.env`

---

## 8. Email (SMTP via Gmail)

1. Use a Gmail account (e.g. `noreply@bdcode.in` or any Gmail)
2. Enable **2-Factor Authentication** on the Google account
3. Generate an **App Password:**
   - Go to [Google Account](https://myaccount.google.com/) → Security → 2-Step Verification → App Passwords
   - Select "Mail" → Generate
   - Copy the 16-character password

**Update `.env`:**
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@bdcode.in
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
SMTP_FROM_EMAIL=your-email@bdcode.in
SMTP_FROM_NAME=bdcode Team
```

**Alert recipients** (comma-separated emails that receive low-rating alerts):
```
ALERT_EMAILS=sales@bdcode.in,marketing@bdcode.in
```

- [ ] Gmail account ready with 2FA enabled
- [ ] App Password generated
- [ ] All SMTP fields set in `.env`
- [ ] `ALERT_EMAILS` set in `.env`

---

## 9. Webhook Security

Generate a random secret string (any strong random value):

```
WEBHOOK_SECRET=your-strong-random-secret-here
```

> This protects `/api/webhook/form` — only requests with the matching
> `X-Webhook-Secret` header will be processed. You'll use the same
> value in Google Apps Script (Step 11).

- [ ] `WEBHOOK_SECRET` set in `.env`

---

## 10. ngrok (For Local Development)

Google Apps Script and WhatsApp need to reach your local server over the internet.

1. Download ngrok: [https://ngrok.com/download](https://ngrok.com/download)
2. Sign up for a free account and authenticate:
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```
3. Start the tunnel:
   ```bash
   ngrok http 8000
   ```
4. Copy the HTTPS URL (e.g. `https://abc123.ngrok.io`)

**Update `.env`:**
```
APP_BASE_URL=https://abc123.ngrok.io
```

> **Note:** ngrok URL changes every time you restart it (free tier).
> Update `WEBHOOK_URL` in Google Apps Script and `APP_BASE_URL` in `.env` each time.

- [ ] ngrok installed
- [ ] ngrok account authenticated
- [ ] `APP_BASE_URL` updated in `.env` with ngrok URL

---

## 11. Google Apps Script Trigger

This connects form submissions to your backend.

1. Open your Form Responses Google Sheet
2. Go to **Extensions → Apps Script**
3. Delete any existing code
4. Paste the contents of `scripts/google_apps_script.js`
5. **Update line 27** — set `WEBHOOK_URL`:
   ```javascript
   const WEBHOOK_URL = 'https://your-ngrok-url.ngrok.io/api/webhook/form';
   ```
6. **Update line 33** — set `WEBHOOK_SECRET` (must match `.env`):
   ```javascript
   const WEBHOOK_SECRET = 'your-strong-random-secret-here';
   ```
7. Click **Run → `onFormSubmit`** (to authorize permissions — accept all prompts)
8. Go to **Triggers** (clock icon on the left) → **Add Trigger:**
   - Function: `onFormSubmit`
   - Event source: `From spreadsheet`
   - Event type: `On form submit`
9. Save

**Test it:**
- Run `testWebhook()` from the Apps Script editor
- Check your backend terminal for the incoming request

- [ ] Apps Script code pasted
- [ ] `WEBHOOK_URL` updated (ngrok or production URL)
- [ ] `WEBHOOK_SECRET` updated (matches `.env`)
- [ ] Permissions authorized (ran `onFormSubmit` once manually)
- [ ] Trigger created (on form submit)
- [ ] `testWebhook()` ran successfully

---

## 12. WhatsApp Business API (Optional — Set Up Later)

The system falls back to email when WhatsApp is not configured. Set this up when ready.

1. Create a [Meta Business Account](https://business.facebook.com/)
2. Go to [Meta Developer Portal](https://developers.facebook.com/) → Create App → Business type
3. Add "WhatsApp" product to your app
4. Set up a test phone number (Meta provides one for development)
5. Get your **Access Token** and **Phone Number ID** from the WhatsApp dashboard
6. Configure webhook URL:
   - URL: `https://your-domain.com/api/webhook/whatsapp`
   - Verify token: same value as `WHATSAPP_VERIFY_TOKEN` in `.env`
   - Subscribe to: `messages`
7. Create message templates (Meta requires approval):
   - Consent request template
   - Reminder template

**Update `.env`:**
```
WHATSAPP_ACCESS_TOKEN=your-access-token-from-meta
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_VERIFY_TOKEN=any-random-string-you-choose
WHATSAPP_API_VERSION=v18.0
```

- [ ] Meta Business Account created
- [ ] WhatsApp Business API app created
- [ ] Phone number registered
- [ ] Access token obtained
- [ ] Webhook URL configured and verified
- [ ] Message templates submitted for approval
- [ ] All WhatsApp fields set in `.env`

---

## 13. Additional `.env` Settings

These have sensible defaults but can be adjusted:

```
# Rating threshold (submissions below this trigger internal alerts)
RATING_THRESHOLD=8.0

# Token expiry (days before review links stop working)
CONSENT_TOKEN_EXPIRY_DAYS=14

# Default country code for WhatsApp numbers without a + prefix
DEFAULT_COUNTRY_CODE=+91

# Set to "production" when deploying to a server
ENVIRONMENT=development
```

- [ ] `RATING_THRESHOLD` reviewed (default: 8.0)
- [ ] `CONSENT_TOKEN_EXPIRY_DAYS` reviewed (default: 14)
- [ ] `DEFAULT_COUNTRY_CODE` reviewed (default: +91)
- [ ] `ENVIRONMENT` set appropriately

---

## 14. Run the Application

### Backend (Terminal 1)
```bash
conda activate review-generator
cd "d:\@White Mastery Systems\Automated Review Generator"
uvicorn backend.main:app --reload --port 8000
```

### Frontend (Terminal 2)
```bash
cd "d:\@White Mastery Systems\Automated Review Generator\frontend"
npm run dev
```

### ngrok (Terminal 3 — for local dev only)
```bash
ngrok http 8000
```

- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on : `https://feedback.bdcode.in/`
- [ ] ngrok tunnel active (if testing with Google Apps Script)

---

## 15. Verify Everything Works

### Health Check
```bash
curl http://localhost:8000/health
```
All dependencies should show `"configured"`.

### API Docs
Open [http://localhost:8000/docs](http://localhost:8000/docs) — interactive Swagger UI.

### Simulated Form Submission
```bash
curl -X POST http://localhost:8000/api/webhook/form ^
  -H "Content-Type: application/json" ^
  -H "X-Webhook-Secret: YOUR_SECRET" ^
  -d "{\"row_number\": 2, \"timestamp\": \"2026-02-13\", \"email\": \"test@example.com\", \"q1_kickoff_satisfaction\": 9, \"q2_communication\": 9, \"q3_project_management\": 8, \"q4_design_ux\": 9, \"q5_technical_quality\": 8, \"q6_launch_smoothness\": 9, \"q7_support_handover\": 8, \"q8_overall_satisfaction\": 9, \"q9_testimonial_consent\": \"Yes\", \"q10_open_feedback\": \"Great team!\"}"
```

### Landing Page
Open [https://automated-review-generator.vercel.app/review/test-token](https://automated-review-generator.vercel.app/review/test-token) — will show error until real data exists.

### End-to-End Test
1. Submit the Google Form with a test response
2. Check backend terminal for processing logs
3. Check the Form Responses Sheet for system-written columns (N onward)
4. Check your email for the review draft (or WhatsApp if configured)
5. Click the landing page link → verify copy + redirect works

- [ ] Health check passes (all configured)
- [ ] Simulated submission returns success
- [ ] Real form submission triggers the full pipeline
- [ ] Email/WhatsApp notification received
- [ ] Landing page displays review and copy works
- [ ] Google Business Profile review page opens after copy

---

## Complete `.env` Template

```env
# --- Gemini AI ---
GEMINI_API_KEY=

# --- Google Business Profile ---
GBP_REVIEW_URL=

# --- Google Sheets ---
FORM_RESPONSES_SHEET_ID=
CRM_SHEET_ID=
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json

# --- WhatsApp Business API (optional) ---
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_VERIFY_TOKEN=
WHATSAPP_API_VERSION=v18.0
WHATSAPP_TEMPLATE_NAME=review_consent
WHATSAPP_TEMPLATE_NAME_APPROVED=review_approved
WHATSAPP_TEMPLATE_LANGUAGE=en

# --- Email (SMTP) ---
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=bdcode Team

# --- Internal Alerts ---
ALERT_EMAILS=

# --- Qualification ---
RATING_THRESHOLD=8.0

# --- Application ---
APP_BASE_URL=http://localhost:8000
FRONTEND_URL=https://automated-review-generator.vercel.app

# --- Webhook Security ---
WEBHOOK_SECRET=

# --- Token Expiry ---
CONSENT_TOKEN_EXPIRY_DAYS=14

# --- Phone Number ---
DEFAULT_COUNTRY_CODE=+91

# --- Environment ---
ENVIRONMENT=development
```
