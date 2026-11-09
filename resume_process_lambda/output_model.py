from pydantic import BaseModel, field_validator, model_validator


class OutputModel(BaseModel):
    is_resume: bool
    score: float
    description: str

    @field_validator("score")
    @classmethod
    def validate_score(cls, value):
        if value < 0.0 or value > 100:
            raise ValueError("Score must be in [0; 100]")
        return value

    @model_validator(mode="after")
    def zero_score_if_not_resume(self):
        if not self.is_resume:
            self.score = 0.0
        return self
