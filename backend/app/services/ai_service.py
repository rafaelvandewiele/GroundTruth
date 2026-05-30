import json
import anthropic
from app.core.config import settings
from app.models.schemas import ClaimResult, Source

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

EXTRACT_SYSTEM_PROMPT = """
You are a fact-checking assistant. Your job is to extract verifiable factual claims from text.

Rules:
- Only extract claims that can be verified (facts, statistics, events, scientific statements)
- Ignore opinions, feelings, predictions, and subjective statements
- Return a JSON array of strings, each being one verifiable claim
- Maximum 3 claims per text
- Translate all claims to English for consistent processing
- Return ONLY the JSON array, no other text

Example output:
["The Eiffel Tower is 330 meters tall", "France has a population of 68 million"]
"""

CHECK_SYSTEM_PROMPT = """
You are a rigorous fact-checker. Given a claim and supporting search results, determine if the claim is true.

Return a JSON object with exactly these fields:
{
  "verdict": "true" | "false" | "nuanced" | "unverifiable",
  "explanation": "Clear explanation in the user's language (2-4 sentences)",
  "confidence": <integer 0-100>
}

Guidelines:
- "true": claim is accurate based on evidence
- "false": claim is demonstrably incorrect
- "nuanced": claim has partial truth or missing context
- "unverifiable": insufficient evidence to judge
- explanation must be in the SAME LANGUAGE as specified
- confidence reflects certainty of your verdict
- Return ONLY the JSON object, no other text
"""


async def extract_claims_from_text(text: str) -> list[str]:
    """Extract verifiable claims from raw text."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=EXTRACT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Extract verifiable claims from:\n\n{text}"}],
    )
    raw = message.content[0].text.strip()
    try:
        claims = json.loads(raw)
        return claims if isinstance(claims, list) else []
    except json.JSONDecodeError:
        return [text[:300]]  # fallback: treat whole text as one claim


async def extract_text_from_image(image_base64: str) -> str:
    """Use Claude Vision to extract text from a screenshot."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Extract all text from this screenshot. Return only the raw text, no commentary.",
                    },
                ],
            }
        ],
    )
    return message.content[0].text.strip()


async def check_claim(
    claim: str,
    search_results: str,
    language: str,
) -> ClaimResult:
    """Fact-check a single claim using search results as context."""
    user_prompt = f"""
Claim to verify: "{claim}"

Search results:
{search_results}

Language for explanation: {language}
"""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=CHECK_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw = message.content[0].text.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {
            "verdict": "unverifiable",
            "explanation": "Could not process this claim.",
            "confidence": 0,
        }

    verdict_en = data.get("verdict", "unverifiable")
    verdict_map = {
        "true": "waar",
        "false": "onwaar",
        "nuanced": "genuanceerd",
        "unverifiable": "onverifieerbaar",
    }

    return ClaimResult(
        claim=claim,
        verdict=verdict_map.get(verdict_en, "onverifieerbaar"),
        verdict_en=verdict_en,
        explanation=data.get("explanation", ""),
        confidence=data.get("confidence", 50),
        sources=[],  # sources are added by the search service
    )
