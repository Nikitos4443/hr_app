from sqlalchemy.orm import Session

from hr_core.models.text_verification_model import TextVerification as TextVerificationModel
from hr_core.repository_interfaces.ITextVerificationRepository import ITextVerificationRepository
from hr_core.sql.tables.text_verification import TextVerification


class SQLTextVerificationRepository(ITextVerificationRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: TextVerificationModel) -> TextVerificationModel:
        row = TextVerification(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return TextVerificationModel.model_validate(row)
