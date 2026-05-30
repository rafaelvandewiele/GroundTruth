import uuid
from datetime import datetime, timezone

from app.models.schemas import CheckRequest, CheckResponse, ClaimResult
from app.services.ai_service import (
    extract_claims_from_text,
    extract_text_from_image,
    check_claim,
)
from app.services.search_service import search_claim
from app.services.cache_service import (
    get_cached_result,
    save_result,
    get_user_check_count,
    increment_user_check_count,
)
from app.services.language_service import detect_language
from app.core.config import settings


async def run_fact_check(request: CheckRequest) -> CheckResponse:
    """
    Full pipeline:
    1. Check cache
    2. Extract text from image (if needed)
    3. Detect language
    4. Extract claims
    5. For each claim: search + AI verdict
    6. Save to cache
    7. Return result
    """

    # Step 1: Check daily limit for logged-in users
    if request.user_id:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        count = await get_user_check_count(request.user_id, today)
        if count >= settings.daily_free_checks:
            raise ValueError(
                f"Daily limit of {settings.daily_free_checks} checks reached. Upgrade for unlimited."
            )

    # Step 2: Extract text from image if provided
    input_text = request.text
    if request.image_base64 and not input_text.strip():
        input_text = await extract_text_from_image(request.image_base64)

    if not input_text.strip():
        raise ValueError("No text provided to check.")

    # Step 3: Check cache
    cached = await get_cached_result(input_text)
    if cached:
        return cached

    # Step 4: Detect language
    lang_code, lang_name = detect_language(input_text)

    # Step 5: Extract individual claims
    claims_text = await extract_claims_from_text(input_text)

    # Step 6: Fact-check each claim (max 3)
    results: list[ClaimResult] = []
    for claim in claims_text[:3]:
        search_text, sources = await search_claim(claim)
        result = await check_claim(claim, search_text, lang_name)
        result.sources = sources
        results.append(result)

    # Step 7: Build response
    response = CheckResponse(
        id=str(uuid.uuid4()),
        original_text=input_text,
        language=lang_code,
        claims=results,
        created_at=datetime.now(timezone.utc),
        cached=False,
    )

    # Step 8: Save to cache + increment user counter
    await save_result(input_text, response)
    if request.user_id:
        await increment_user_check_count(request.user_id, today)

    return response
