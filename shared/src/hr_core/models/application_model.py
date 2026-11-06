from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Application(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    vacancy_id: int
    email: str
    full_name: str
    status: str = "pending"
    created_at: datetime | None = None
