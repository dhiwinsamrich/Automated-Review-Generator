/**
 * Google Apps Script — Form Submission Webhook Trigger
 *
 * Install this script on the Google Sheet linked to your feedback form.
 * It fires on every form submission and POSTs the data to your FastAPI backend.
 *
 * Setup Instructions:
 * 1. Open your Google Sheet (linked to the feedback form)
 * 2. Go to Extensions → Apps Script
 * 3. Paste this entire file into the script editor
 * 4. Update WEBHOOK_URL below with your FastAPI server URL
 * 5. Click Run → onFormSubmit (to authorize permissions)
 * 6. Go to Triggers (clock icon) → Add Trigger:
 *    - Function: onFormSubmit
 *    - Event source: From spreadsheet
 *    - Event type: On form submit
 * 7. Save and test with a form submission
 */

// ─── Configuration ───────────────────────────────────────

/**
 * Your FastAPI webhook URL.
 * For local development with ngrok: https://xxxx.ngrok.io/api/webhook/form
 * For production: https://your-server.com/api/webhook/form
 */
const WEBHOOK_URL = 'http://localhost:8000/api/webhook/form';

/**
 * Optional: webhook secret for request authentication.
 * Must match WEBHOOK_SECRET in your .env file.
 */
const WEBHOOK_SECRET = '';


// ─── Main Trigger Function ───────────────────────────────

/**
 * Fires automatically when a form response is submitted.
 * Extracts the response data and POSTs it to the FastAPI backend.
 *
 * @param {Object} e - Form submit event object
 */
function onFormSubmit(e) {
    var sheet = e.source.getActiveSheet();
    var row = e.range.getRow();

    try {
        // Get the submitted row data
        var rowData = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];

        // Build the payload matching FormSubmissionData schema
        var payload = {
            row_number: row,
            timestamp: rowData[0] ? rowData[0].toString() : new Date().toISOString(),
            email: rowData[1] || '',                     // Column B: Auto-captured email

            // LinkedIn profile
            linkedin_profile: rowData[2] || '',          // Column C: LinkedIn profile

            // Q1-Q8 ratings (columns D-K, 1-10 scale)
            q1_kickoff_satisfaction: parseFloat(rowData[3]) || null,   // Column D
            q2_communication: parseFloat(rowData[4]) || null,          // Column E
            q3_project_management: parseFloat(rowData[5]) || null,     // Column F
            q4_design_ux: parseFloat(rowData[6]) || null,              // Column G
            q5_technical_quality: parseFloat(rowData[7]) || null,      // Column H
            q6_launch_smoothness: parseFloat(rowData[8]) || null,      // Column I
            q7_support_handover: parseFloat(rowData[9]) || null,       // Column J
            q8_overall_satisfaction: parseFloat(rowData[10]) || null,   // Column K

            // Q9: Testimonial consent (column L)
            q9_testimonial_consent: rowData[11] || 'No',

            // Q10: Open feedback (column M)
            q10_open_feedback: rowData[12] || '',

            // Include the sheet ID so the backend can write back
            sheet_id: sheet.getParent().getId()
        };

        // Send to FastAPI backend
        var options = {
            method: 'post',
            contentType: 'application/json',
            payload: JSON.stringify(payload),
            muteHttpExceptions: true,
            headers: {}
        };

        // Add webhook secret if configured
        if (WEBHOOK_SECRET) {
            options.headers['X-Webhook-Secret'] = WEBHOOK_SECRET;
        }

        var response = UrlFetchApp.fetch(WEBHOOK_URL, options);
        var statusCode = response.getResponseCode();
        var responseBody = response.getContentText();

        // Log the result
        Logger.log('Webhook response [' + statusCode + ']: ' + responseBody);

        if (statusCode !== 200) {
            Logger.log('WARNING: Webhook returned non-200 status: ' + statusCode);
        }

    } catch (error) {
        Logger.log('ERROR in onFormSubmit: ' + error.message);

        // Optionally send an error alert email
        try {
            MailApp.sendEmail(
                Session.getActiveUser().getEmail(),
                '[Review Generator] Form Webhook Error',
                'Error processing form submission at row ' + row + ':\n\n' + error.message
            );
        } catch (emailError) {
            Logger.log('Could not send error alert: ' + emailError.message);
        }
    }
}


// ─── Utility Functions ───────────────────────────────────

/**
 * Test function — manually trigger the webhook with the last submitted row.
 * Run this from the Apps Script editor to test your setup.
 */
function testWebhook() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var lastRow = sheet.getLastRow();

    if (lastRow < 2) {
        Logger.log('No data rows found. Submit a form response first.');
        return;
    }

    // Simulate the onFormSubmit event
    var mockEvent = {
        source: SpreadsheetApp.getActiveSpreadsheet(),
        range: sheet.getRange(lastRow, 1)
    };

    Logger.log('Testing webhook with row ' + lastRow);
    onFormSubmit(mockEvent);
}


/**
 * View the column mapping for debugging.
 * Run this to see which columns map to which fields.
 */
function showColumnMapping() {
    var mapping = [
        'A: Timestamp (auto)',
        'B: Email (auto-captured Google account)',
        'C: LinkedIn Profile',
        'D: Q1 - Kickoff Satisfaction (1-10)',
        'E: Q2 - Communication (1-10)',
        'F: Q3 - Project Management (1-10)',
        'G: Q4 - Design & UX (1-10)',
        'H: Q5 - Technical Quality (1-10)',
        'I: Q6 - Launch Smoothness (1-10)',
        'J: Q7 - Support & Handover (1-10)',
        'K: Q8 - Overall Satisfaction (1-10)',
        'L: Q9 - Testimonial Consent (Yes/No)',
        'M: Q10 - Open Feedback (text)',
        '',
        '--- System-written columns (by FastAPI) ---',
        'N: Average Rating',
        'O: Qualified (YES/NO)',
        'P: Client Name (from CRM)',
        'Q: Company (from CRM)',
        'R: Services (from CRM)',
        'S: WhatsApp (from CRM)',
        'T: Business Email (from CRM)',
        'U: Draft Text (AI generated)',
        'V: Consent Token',
        'W: Status (PENDING/SENT/APPROVED/DECLINED/COPIED)',
        'X: Delivery Method (WHATSAPP/EMAIL)',
        'Y: Sent At',
        'Z: Copied At',
        'AA: Error Log'
    ];

    Logger.log(mapping.join('\n'));
}
