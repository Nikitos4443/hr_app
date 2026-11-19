from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from hr_core.models.application_model import ApplicationSummary

ApplicationStatus = Literal["pending", "invited", "shortlisted", "rejected"]
ApplicationAction = Literal["invite", "shortlist", "reject"]
ScreeningState = Literal["not_invited", "invited", "in_progress", "completed"]


class ApplicationListItem(BaseModel):
    id: int
    email: str
    full_name: str | None
    status: ApplicationStatus
    created_at: datetime | None
    resume_status: str | None
    resume_score: float | None
    screening_state: ScreeningState
    answered_count: int
    total_questions: int
    rank: int | None
    ai_summary: str | None

    @classmethod
    def from_summary(cls, summary: ApplicationSummary, total_questions: int) -> ApplicationListItem:
        if summary.screening_invited_at is None:
            state: ScreeningState = "not_invited"
        elif total_questions > 0 and summary.answered_count >= total_questions:
            state = "completed"
        elif summary.answered_count > 0:
            state = "in_progress"
        else:
            state = "invited"
        return cls(
            **summary.model_dump(exclude={"screening_invited_at"}),
            screening_state=state,
            total_questions=total_questions,
        )


class ApplicationCounts(BaseModel):
    all: int = 0
    pending: int = 0
    invited: int = 0
    shortlisted: int = 0
    rejected: int = 0


class ApplicationListResponse(BaseModel):
    items: list[ApplicationListItem]
    total: int
    counts: ApplicationCounts


class ResumeReview(BaseModel):
    """What resume_process_lambda stores in ResumeVerification.llm_review (OutputModel)."""

    is_resume: bool | None = None
    score: float | None = None
    description: str | None = None


class ResumeDetail(BaseModel):
    status: str | None
    score: float | None
    review: ResumeReview | None
    file_url: str | None = Field(description="Short-lived presigned GET for the resume PDF")


class AnswerDetail(BaseModel):
    question_id: int
    order: int
    type: Literal["video", "text"]
    text: str
    status: str  # pending | done
    answer: str | None = None
    transcription: str | None = None


class TimelineEvent(BaseModel):
    type: Literal[
        "applied",
        "resume_processed",
        "screening_invited",
        "screening_completed",
        "shortlisted",
        "rejected",
        "rejection_notified",
    ]
    at: datetime


class ApplicationDetailResponse(BaseModel):
    id: int
    vacancy_id: int
    email: str
    full_name: str | None
    status: ApplicationStatus
    created_at: datetime | None
    resume: ResumeDetail
    rank: int | None
    ai_summary: str | None
    answers: list[AnswerDetail]
    timeline: list[TimelineEvent]


class ApplicationActionResult(BaseModel):
    id: int
    status: ApplicationStatus
    screening_invited_at: datetime | None
    status_changed_at: datetime | None


class BulkActionDTO(BaseModel):
    ids: list[int] = Field(min_length=1, max_length=200)
    action: ApplicationAction


class BulkFailure(BaseModel):
    id: int
    detail: str


class BulkActionResponse(BaseModel):
    updated: list[int]
    failed: list[BulkFailure]
