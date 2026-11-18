from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from hr_core.models.question_model import Question
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from hr_core.sql.tables.questions import Questions
from hr_core.sql.tables.text_verification import TextVerification
from hr_core.sql.tables.video_verification import VideoVerification


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

    def replace_for_vacancy(self, vacancy_id: int, entities: list[Question]) -> list[Question]:
        self.db.execute(delete(Questions).where(Questions.vacancy_id == vacancy_id))
        rows = [Questions(**e.model_dump(exclude={"id"})) for e in entities]
        self.db.add_all(rows)
        self.db.commit()
        for row in rows:
            self.db.refresh(row)
        return [Question.model_validate(row) for row in rows]

    def has_answers(self, vacancy_id: int) -> bool:
        question_ids = select(Questions.id).where(Questions.vacancy_id == vacancy_id)
        for table in (TextVerification, VideoVerification):
            found = self.db.scalar(
                select(table.id).where(table.question_id.in_(question_ids)).limit(1)
            )
            if found is not None:
                return True
        return False

    def count_by_vacancies(self, vacancy_ids: list[int]) -> dict[int, int]:
        if not vacancy_ids:
            return {}
        rows = self.db.execute(
            select(Questions.vacancy_id, func.count())
            .where(Questions.vacancy_id.in_(vacancy_ids))
            .group_by(Questions.vacancy_id)
        )
        return dict(rows.all())
