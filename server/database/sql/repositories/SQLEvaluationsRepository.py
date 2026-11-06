from sqlalchemy.orm import Session

from database.models.evaluation_model import Evaluation
from database.repository_interfaces.IEvaluationsRepository import IEvaluationsRepository
from database.sql.tables.evaluations import Evaluations


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
