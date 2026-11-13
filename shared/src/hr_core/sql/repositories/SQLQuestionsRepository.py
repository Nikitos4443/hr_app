from sqlalchemy import select
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

    def get_by_id(self, question_id: int) -> Question | None:
        row = self.db.get(Questions, question_id)
        return None if row is None else Question.model_validate(row)

    def list_by_vacancy(self, vacancy_id: int) -> list[Question]:
        rows = self.db.scalars(
            select(Questions).where(Questions.vacancy_id == vacancy_id).order_by(Questions.order)
        )
        return [Question.model_validate(row) for row in rows]
