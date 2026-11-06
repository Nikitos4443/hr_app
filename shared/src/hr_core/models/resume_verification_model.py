from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ResumeVerification(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    application_id: int
    status: str = "pending"
    s3_key: str | None = None
    score: float | None = None
    llm_review: dict[str, Any] | None = None
    processed_at: datetime | None = None
