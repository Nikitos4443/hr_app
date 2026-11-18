from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from hr_core.models.evaluation_model import Evaluation
from hr_core.repository_interfaces.IEvaluationsRepository import IEvaluationsRepository
from hr_core.sql.tables.evaluations import Evaluations


class SQLEvaluationsRepository(IEvaluationsRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: Evaluation) -> Evaluation:
        row = Evaluations(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return Evaluation.model_validate(row)

    def replace_for_vacancy(self, vacancy_id: int, entities: list[Evaluation]) -> list[Evaluation]:
        self.db.execute(delete(Evaluations).where(Evaluations.vacancy_id == vacancy_id))
        rows = [Evaluations(**e.model_dump(exclude={"id"}, exclude_none=True)) for e in entities]
        self.db.add_all(rows)
        self.db.commit()
        for row in rows:
            self.db.refresh(row)
        return [Evaluation.model_validate(row) for row in rows]

    def delete_by_application(self, application_id: int) -> None:
        self.db.execute(delete(Evaluations).where(Evaluations.application_id == application_id))
        self.db.commit()

    def get_by_application(self, application_id: int) -> Evaluation | None:
        row = self.db.scalar(
            select(Evaluations).where(Evaluations.application_id == application_id)
        )
        return None if row is None else Evaluation.model_validate(row)
