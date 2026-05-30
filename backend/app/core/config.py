from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    supabase_url: str
    supabase_service_key: str
    environment: str = "development"
    daily_free_checks: int = 10
    cache_similarity_threshold: float = 0.92

    class Config:
        env_file = ".env"


settings = Settings()
