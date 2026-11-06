from typing import Literal

from pydantic import BaseModel, ConfigDict


class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    vacancy_id: int
    order: int
    type: Literal["video", "text"]
    text: str
    video_max_duration_sec: int | None = None
