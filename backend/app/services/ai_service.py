import json
import google.generativeai as genai
from app.core.config import settings
from app.models.schemas import ClaimResult, Source

genai.configure(api_key=settings.gemini_api_key)

# Gratis limieten: 1500 requests/dag, 15 requests/minuut
model = genai.GenerativeModel("gemini-1.5-flash")

EXTRACT_PROMPT = """
You are a fact-checking assistant. Extract verifiable factual claims from the text below.

Rules:
- Only extract claims that can be verified (facts, statistics, events, scientific statements)
- Ignore opinions, feelings, predictions, and subjective statements
- Return a JSON array of strings, each being one verifiable claim
- Maximum 3 claims per text
- Translate all claims to English for consistent processing
- Return ONLY the JSON array, no other text

Example output:
["The Eiffel Tower is 330 meters tall", "France has a population of 68 million"]

Text to analyze:
"""

CHECK_PROMPT_TEMPLATE = """
You are a rigorous fact-checker. Given a claim and supporting search results, determine if the claim is true.

Return a JSON object with exactly these fields:
{{
  "verdict": "true" | "false" | "nuanced" | "unverifiable",
  "explanation": "Clear explanation in {language} (2-4 sentences)",
  "confidence": <integer 0-100>
}}

Guidelines:
- "true": claim is accurate based on evidence
- "false": claim is demonstrably incorrect
- "nuanced": claim has partial truth or missing context
- "unverifiable": insufficient evidence to judge
- confidence reflects certainty of your verdict
- Return ONLY the JSON object, no other text

Claim to verify: "{claim}"

Search results:
{search_results}
"""


async def extract_claims_from_text(text: str) -> list[str]:
    """Extract verifiable claims from raw text using Gemini Flash (free)."""
    try:
        response = model.generate_content(EXTRACT_PROMPT + text)
        raw = response.text.strip()
        # Strip possible markdown code fences
        raw = raw.replace("```json", "").replace("```", "").strip()
        claims = json.loads(raw)
        return claims if isinstance(claims, list) else [text[:300]]
    except Exception:
        return [text[:300]]  # fallback: treat whole text as one claim


async def extract_text_from_image(image_base64: str) -> str:
    """Use Gemini Vision to extract text from a screenshot (free)."""
    import base64
    vision_model = genai.GenerativeModel("gemini-1.5-flash")
    image_data = base64.b64decode(image_base64)
    # Gemini accepts PIL images or inline data
    import PIL.Image
    import io
    img = PIL.Image.open(io.BytesIO(image_data))
    response = vision_model.generate_content([
        "Extract all text from this screenshot. Return only the raw text, no commentary.",
        img,
    ])
    return response.text.strip()


async def check_claim(
    claim: str,
    search_results: str,
    language: str,
) -> ClaimResult:
    """Fact-check a single claim using Gemini Flash + search results."""
    prompt = CHECK_PROMPT_TEMPLATE.format(
        language=language,
        claim=claim,
        search_results=search_results,
    )
    try:
        response = model.generate_content(prompt)
        raw = response.text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
    except Exception:
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
        sources=[],
    )
