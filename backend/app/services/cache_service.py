import hashlib
import json
from datetime import datetime, timezone
from supabase import create_client, Client
from app.core.config import settings
from app.models.schemas import CheckResponse

supabase: Client = create_client(settings.supabase_url, settings.supabase_service_key)


def _hash_text(text: str) -> str:
    """Create a consistent hash for cache lookup."""
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()


async def get_cached_result(text: str) -> CheckResponse | None:
    """Look up a previous check by text hash."""
    text_hash = _hash_text(text)
    try:
        result = (
            supabase.table("checks")
            .select("*")
            .eq("text_hash", text_hash)
            .limit(1)
            .execute()
        )
        if result.data:
            row = result.data[0]
            response = CheckResponse(**json.loads(row["response_json"]))
            response.cached = True
            return response
    except Exception:
        pass
    return None


async def save_result(text: str, response: CheckResponse) -> None:
    """Persist a new check result to the database."""
    text_hash = _hash_text(text)
    try:
        supabase.table("checks").insert(
            {
                "text_hash": text_hash,
                "original_text": text[:1000],
                "response_json": response.model_dump_json(),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ).execute()
    except Exception:
        pass  # cache failure is non-fatal


async def get_user_check_count(user_id: str, date: str) -> int:
    """Return how many checks a user has done today."""
    try:
        result = (
            supabase.table("user_usage")
            .select("count")
            .eq("user_id", user_id)
            .eq("date", date)
            .limit(1)
            .execute()
        )
        if result.data:
            return result.data[0]["count"]
    except Exception:
        pass
    return 0


async def increment_user_check_count(user_id: str, date: str) -> None:
    """Increment or create the daily usage counter for a user."""
    try:
        existing = (
            supabase.table("user_usage")
            .select("count")
            .eq("user_id", user_id)
            .eq("date", date)
            .execute()
        )
        if existing.data:
            current = existing.data[0]["count"]
            supabase.table("user_usage").update({"count": current + 1}).eq(
                "user_id", user_id
            ).eq("date", date).execute()
        else:
            supabase.table("user_usage").insert(
                {"user_id": user_id, "date": date, "count": 1}
            ).execute()
    except Exception:
        pass
