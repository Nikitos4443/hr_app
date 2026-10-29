from pydantic import BaseModel
from pydantic import field_validator
class OutputModel(BaseModel):
    score: float
    description: str

    @field_validator("score")
    @classmethod
    def validate_score(cls, value):
        if value < 0.0 or value > 100:
             raise ValueError("Score must be in [0; 100]")
        return value