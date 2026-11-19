from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class Vacancy(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    title: str
    company: str
    company_id: int | None = None
    location: str | None = None
    employment_type: str | None = None
    experience_years_min: int | None = None
    description: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    nice_to_have: list[str] = Field(default_factory=list)
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    status: str = "open"
    created_by: int
    deadline_at: datetime | None = None
    selection_status: str = "pending"  # pending | running | done | failed
    created_at: datetime | None = None

    def deadline_utc(self) -> datetime | None:
        # Some backends (SQLite) drop the timezone; stored deadlines are always UTC.
        if self.deadline_at is not None and self.deadline_at.tzinfo is None:
            return self.deadline_at.replace(tzinfo=UTC)
        return self.deadline_at
