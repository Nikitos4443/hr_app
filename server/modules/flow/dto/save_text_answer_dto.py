from pydantic import BaseModel, ConfigDict, Field

from hr_core.constants.index import MAX_TEXT_ANSWER_LENGTH


class SaveTextAnswerDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    answer: str = Field(min_length=1, max_length=MAX_TEXT_ANSWER_LENGTH)
