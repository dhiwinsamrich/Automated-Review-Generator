"""
Rating qualification logic.

Determines whether a form submission qualifies for AI review generation
based on average rating threshold and testimonial consent.
"""

from backend.config import get_settings
from backend.utils.logger import logger

# Keywords that suggest negative sentiment despite high ratings
_NEGATIVE_KEYWORDS = [
    "terrible", "horrible", "awful", "worst", "never again",
    "disappointed", "waste of time", "waste of money", "regret",
    "unprofessional", "scam", "fraud", "do not recommend",
    "stay away", "avoid", "disaster",
]


def calculate_average(ratings: list) -> float:
    """
    Calculate average rating from Q1-Q8 values (1-10 scale).

    Filters out None and empty values before calculating.

    Args:
        ratings: List of rating values (may contain None).

    Returns:
        Average rating rounded to 2 decimal places, or 0.0 if no valid ratings.
    """
    valid_ratings = []
    for r in ratings:
        if r is not None and str(r).strip() != "":
            try:
                valid_ratings.append(float(r))
            except (ValueError, TypeError):
                continue

    if not valid_ratings:
        return 0.0

    avg = sum(valid_ratings) / len(valid_ratings)
    return round(avg, 2)


def meets_rating_threshold(avg_rating: float) -> bool:
    """Check if the average rating meets the configured threshold."""
    settings = get_settings()
    return avg_rating >= settings.RATING_THRESHOLD


def has_testimonial_consent(consent: str) -> bool:
    """Check if the client gave testimonial consent (Q9 = Yes)."""
    return consent.strip().lower() == "yes"


def check_qualification(avg_rating: float, consent: str) -> bool:
    """
    Check if a submission meets the qualification threshold.

    Qualification requires BOTH:
    - Average rating >= configured threshold (default: 8.0)
    - Q9 testimonial consent = "Yes"

    Args:
        avg_rating: Calculated average from Q1-Q8.
        consent: Q9 response string ("Yes" or "No").

    Returns:
        True if submission qualifies for review generation.
    """
    threshold_met = meets_rating_threshold(avg_rating)
    consent_given = has_testimonial_consent(consent)

    logger.info(
        f"Qualification check: avg={avg_rating}, "
        f"threshold_met={threshold_met}, consent={consent_given} "
        f"→ qualified={threshold_met and consent_given}"
    )

    return threshold_met and consent_given


def has_negative_sentiment(open_feedback: str) -> bool:
    """
    Basic keyword-based check for negative sentiment in open feedback.

    Used to flag cases where a client gives high ratings but writes
    negative comments (BRD edge case EC-01).

    Args:
        open_feedback: Q10 open-text feedback.

    Returns:
        True if negative keywords are detected.
    """
    if not open_feedback:
        return False

    text = open_feedback.lower()
    for keyword in _NEGATIVE_KEYWORDS:
        if keyword in text:
            logger.warning(
                f"Negative sentiment detected in open feedback: '{keyword}'"
            )
            return True

    return False
