from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TextVerification(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    application_id: int
    question_id: int
    status: str = "pending"
    answer: str | None = None
    processed_at: datetime | None = None
