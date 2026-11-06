from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VideoVerification(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    application_id: int
    question_id: int
    status: str = "pending"
    s3_key: str | None = None
    transcription: str | None = None
    processed_at: datetime | None = None
