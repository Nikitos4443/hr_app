from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    description: str | None = None
    website: str | None = None
    created_at: datetime | None = None
