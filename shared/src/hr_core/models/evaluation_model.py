from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Evaluation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    application_id: int
    vacancy_id: int
    order: int | None = None
    summary: str | None = None
    evaluated_at: datetime | None = None
