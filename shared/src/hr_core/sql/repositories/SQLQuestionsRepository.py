from sqlalchemy.orm import Session

from hr_core.models.question_model import Question
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from hr_core.sql.tables.questions import Questions


class SQLQuestionsRepository(IQuestionsRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: Question) -> Question:
        row = Questions(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return Question.model_validate(row)
