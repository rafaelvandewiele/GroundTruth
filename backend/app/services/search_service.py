import httpx
from app.core.config import settings
from app.models.schemas import Source

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"


async def search_claim(claim: str) -> tuple[str, list[Source]]:
    """
    Search for evidence about a claim using Perplexity Sonar.
    Returns (formatted_results_string, list_of_sources).
    """
    headers = {
        "Authorization": f"Bearer {settings.perplexity_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a research assistant. Find factual evidence about the given claim. "
                    "Summarize what the most reliable sources say. Be concise and factual."
                ),
            },
            {
                "role": "user",
                "content": f"Find evidence for or against this claim: {claim}",
            },
        ],
        "return_citations": True,
        "max_tokens": 800,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(PERPLEXITY_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    message = data["choices"][0]["message"]
    content = message.get("content", "")
    citations = data.get("citations", [])

    sources = [
        Source(
            url=c.get("url", ""),
            title=c.get("title", "Source"),
            snippet=c.get("snippet", ""),
        )
        for c in citations[:5]
    ]

    return content, sources
