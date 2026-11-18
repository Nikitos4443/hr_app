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
    status_changed_at: datetime | None = None

    def derived_status(self) -> str:
        """pending | invited | shortlisted | rejected (invited = screening_invited_at set)."""
        if self.status in ("rejected", "shortlisted"):
            return self.status
        return "invited" if self.screening_invited_at is not None else "pending"


class ApplicationSummary(BaseModel):
    """One row of the staff applications list, joined with resume, screening and ranking."""

    id: int
    email: str
    full_name: str | None = None
    status: str  # pending | invited | shortlisted | rejected
    created_at: datetime | None = None
    resume_status: str | None = None
    resume_score: float | None = None
    screening_invited_at: datetime | None = None
    answered_count: int = 0
    rank: int | None = None
    ai_summary: str | None = None
