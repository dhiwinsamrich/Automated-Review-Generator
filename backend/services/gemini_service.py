"""
Gemini AI service for generating personalized review drafts.

Uses google-generativeai SDK with retry logic and word count validation.
"""

import asyncio

import google.generativeai as genai

from backend.config import get_settings
from backend.prompts.review_generation import SYSTEM_PROMPT, build_review_prompt
from backend.utils.logger import logger


async def generate_review_draft(
    client_name: str,
    company: str,
    services: str,
    avg_rating: float,
    ratings_breakdown: dict,
    open_feedback: str = "",
) -> str:
    """
    Generate a personalized review draft using Gemini AI.

    Constructs a prompt from client + form data, calls Gemini,
    and retries up to 3 times on failure with exponential backoff.

    Args:
        client_name: Client's full name.
        company: Client's company name.
        services: Services used by the client.
        avg_rating: Average rating across Q1-Q8.
        ratings_breakdown: Individual Q1-Q8 ratings dict.
        open_feedback: Q10 open-text feedback.

    Returns:
        Generated review draft as a string.

    Raises:
        Exception: If all retry attempts fail.
    """
    settings = get_settings()

    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured")

    # Configure the SDK
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Build the prompt
    user_prompt = build_review_prompt(
        client_name=client_name,
        company=company,
        services=services,
        avg_rating=avg_rating,
        ratings_breakdown=ratings_breakdown,
        open_feedback=open_feedback,
    )

    full_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}"

    # Retry logic with exponential backoff
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Gemini API call attempt {attempt}/{max_retries}")

            response = await asyncio.to_thread(
                model.generate_content,
                full_prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.7,
                ),
            )

            draft = response.text.strip()

            # Clean up: remove surrounding quotes if model adds them
            if draft.startswith('"') and draft.endswith('"'):
                draft = draft[1:-1]
            if draft.startswith("'") and draft.endswith("'"):
                draft = draft[1:-1]

            # Validate word count (target: 20-80 words)
            word_count = len(draft.split())
            logger.info(
                f"Review draft generated: {word_count} words (target: 20-80)"
            )

            if word_count < 15 or word_count > 100:
                logger.warning(
                    f"Draft word count {word_count} outside acceptable range, "
                    f"retrying..."
                )
                if attempt < max_retries:
                    continue
                # On final attempt, accept whatever we got
                logger.warning("Final attempt — accepting draft as-is")

            return draft

        except Exception as e:
            logger.error(f"Gemini API attempt {attempt} failed: {e}")
            if attempt == max_retries:
                raise
            backoff = 2**attempt
            logger.info(f"Retrying in {backoff}s...")
            await asyncio.sleep(backoff)

    raise Exception("Failed to generate review draft after all retries")
