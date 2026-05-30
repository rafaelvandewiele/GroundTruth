from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class CheckRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    image_base64: Optional[str] = None  # for screenshot input


class Source(BaseModel):
    url: str
    title: str
    snippet: str


class ClaimResult(BaseModel):
    claim: str
    verdict: Literal["waar", "onwaar", "genuanceerd", "onverifieerbaar"]
    verdict_en: Literal["true", "false", "nuanced", "unverifiable"]
    explanation: str
    confidence: int  # 0-100
    sources: list[Source]


class CheckResponse(BaseModel):
    id: str
    original_text: str
    language: str
    claims: list[ClaimResult]
    created_at: datetime
    cached: bool = False


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
