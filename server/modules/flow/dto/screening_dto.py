from typing import Literal

from pydantic import BaseModel


class ScreeningQuestion(BaseModel):
    id: int
    order: int
    type: Literal["video", "text"]
    text: str
    video_max_duration_sec: int | None = None
    answered: bool


class ScreeningResponse(BaseModel):
    """What a candidate may see about their own screening; nothing internal."""

    vacancy_title: str
    company_name: str
    status: str
    screening_progress: Literal["in_progress", "completed"]
    questions: list[ScreeningQuestion]
