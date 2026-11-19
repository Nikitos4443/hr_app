from typing import Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator

MIN_VIDEO_DURATION_SEC = 10
MAX_VIDEO_DURATION_SEC = 600
MAX_QUESTIONS = 50


class QuestionInputDTO(BaseModel):
    """One screening question; `order` is assigned by the server from the list position."""

    type: Literal["video", "text"]
    text: str = Field(max_length=2000)
    video_max_duration_sec: int | None = None

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must not be empty")
        return value

    @model_validator(mode="after")
    def check_duration(self) -> Self:
        if self.type == "video":
            duration = self.video_max_duration_sec
            if duration is None or not MIN_VIDEO_DURATION_SEC <= duration <= MAX_VIDEO_DURATION_SEC:
                raise ValueError(
                    "video_max_duration_sec must be between "
                    f"{MIN_VIDEO_DURATION_SEC} and {MAX_VIDEO_DURATION_SEC} for video questions"
                )
        elif self.video_max_duration_sec is not None:
            raise ValueError("video_max_duration_sec must be null for text questions")
        return self
