from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Application(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    vacancy_id: int
    email: str
    full_name: str | None = None
    status: str = "pending"
    created_at: datetime | None = None
    screening_token: str | None = None
    screening_invited_at: datetime | None = None
    rejection_notified_at: datetime | None = None
    purged_at: datetime | None = None
