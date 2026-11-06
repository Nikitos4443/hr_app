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
