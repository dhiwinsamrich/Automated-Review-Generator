"""
Gemini AI prompt templates for review generation.

Kept in a separate file for easy maintenance and iteration.
"""


# ─── System Prompt ────────────────────────────────────────

SYSTEM_PROMPT = """You are a professional copywriter helping B2B clients write authentic \
Google Business Profile reviews. Generate a review draft that:

- Is 100-200 words long
- Uses first-person voice (written from the client's perspective)
- Sounds natural and authentic — NOT robotic or generic
- Has a professional B2B tone appropriate for business/technology services
- Avoids keyword stuffing and exaggerated claims
- Mentions specific aspects of the service experience based on the data provided
- Is suitable for Google Business Profile (no star ratings in text)
- Does NOT use cliché phrases like "I highly recommend" more than once
- Does NOT start with "I" — vary the opening

The review should feel like something a real business professional would write \
about their experience working with a technology partner."""


# ─── User Prompt Builder ─────────────────────────────────

def build_review_prompt(
    client_name: str,
    company: str,
    services: str,
    avg_rating: float,
    ratings_breakdown: dict,
    open_feedback: str = "",
) -> str:
    """
    Build the user prompt for Gemini to generate a review draft.

    Args:
        client_name: Client's full name from CRM.
        company: Client's company name from CRM.
        services: Services used (from CRM).
        avg_rating: Calculated average across Q1-Q8.
        ratings_breakdown: Dict with q1-q8 individual scores.
        open_feedback: Q10 open-text feedback from the form.

    Returns:
        Formatted prompt string ready for Gemini API.
    """
    prompt = f"""Write a Google Business Profile review for **bdcode** from the perspective of:

- Client Name: {client_name}
- Company: {company or "a business client"}
- Service Used: {services or "digital/technology services"}
- Overall Satisfaction: {avg_rating:.1f}/10

Rating Breakdown (each out of 10):
- Initial Kickoff & Goal Understanding: {_fmt(ratings_breakdown.get("q1"))}
- Communication & Responsiveness: {_fmt(ratings_breakdown.get("q2"))}
- Project Planning & Management: {_fmt(ratings_breakdown.get("q3"))}
- Design, Branding & UX: {_fmt(ratings_breakdown.get("q4"))}
- Technical Quality & Performance: {_fmt(ratings_breakdown.get("q5"))}
- Testing & Launch Smoothness: {_fmt(ratings_breakdown.get("q6"))}
- Training, Handover & Support: {_fmt(ratings_breakdown.get("q7"))}
- Overall Satisfaction: {_fmt(ratings_breakdown.get("q8"))}
"""

    # Add open feedback if provided — this adds specificity to the draft
    if open_feedback and open_feedback.strip():
        prompt += f"""
The client also shared this specific feedback:
\"{open_feedback}\"

Incorporate the sentiment and any specific details from this feedback into the review.
"""

    prompt += """
Generate a natural, authentic review that highlights the strongest-rated areas. \
Focus on concrete experiences rather than vague praise. \
The review should feel personal and specific to this client's project."""

    return prompt


def _fmt(value) -> str:
    """Format a rating value for the prompt, handling None."""
    if value is None:
        return "N/A"
    return f"{value}/10"
