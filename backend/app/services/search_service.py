import httpx
from bs4 import BeautifulSoup
from app.models.schemas import Source

DUCKDUCKGO_URL = "https://html.duckduckgo.com/html/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


async def search_claim(claim: str) -> tuple[str, list[Source]]:
    """
    Search DuckDuckGo (gratis, geen API-sleutel nodig) voor bewijs over een bewering.
    Geeft (formatted_results_string, list_of_sources) terug.
    """
    sources: list[Source] = []
    summary_parts: list[str] = []

    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            response = await client.post(
                DUCKDUCKGO_URL,
                data={"q": claim, "kl": "wt-wt"},
                headers=HEADERS,
            )
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".result")[:6]

        for result in results:
            title_tag = result.select_one(".result__title a")
            snippet_tag = result.select_one(".result__snippet")
            url_tag = result.select_one(".result__url")

            title = title_tag.get_text(strip=True) if title_tag else "Source"
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            url = url_tag.get_text(strip=True) if url_tag else ""

            # Reconstruct full URL if needed
            if url and not url.startswith("http"):
                url = "https://" + url

            if title and snippet:
                sources.append(Source(url=url, title=title, snippet=snippet))
                summary_parts.append(f"- {title}: {snippet}")

    except Exception as e:
        # Als DuckDuckGo faalt, geef lege resultaten terug (Gemini baseert zich dan op eigen kennis)
        return f"No search results available. Error: {str(e)}", []

    summary = "\n".join(summary_parts) if summary_parts else "No results found."
    return summary, sources
