from sqlalchemy.orm import Session

from hr_core.models.resume_verification_model import (
    ResumeVerification as ResumeVerificationModel,
)
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from hr_core.sql.tables.resume_verification import ResumeVerification


class SQLResumeVerificationRepository(IResumeVerificationRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: ResumeVerificationModel) -> ResumeVerificationModel:
        row = ResumeVerification(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return ResumeVerificationModel.model_validate(row)
