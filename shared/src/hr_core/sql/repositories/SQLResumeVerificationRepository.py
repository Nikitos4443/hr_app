from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from hr_core.models.resume_verification_model import (
    ResumeVerification as ResumeVerificationModel,
)
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from hr_core.sql.tables.applications import Applications
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

    def save_result(
        self, application_id: int, s3_key: str, score: float, llm_review: dict[str, Any]
    ) -> ResumeVerificationModel:
        row = self.db.scalar(
            select(ResumeVerification).where(ResumeVerification.application_id == application_id)
        )
        if row is None:
            row = ResumeVerification(application_id=application_id)
            self.db.add(row)
        row.s3_key = s3_key
        row.score = score
        row.llm_review = llm_review
        row.status = "done"
        row.processed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(row)
        return ResumeVerificationModel.model_validate(row)

    def count_active(self, vacancy_id: int) -> int:
        return self.db.scalar(
            select(func.count()).select_from(self._active(vacancy_id).subquery())
        )

    def get_lowest_active_below(
        self, vacancy_id: int, threshold: float
    ) -> ResumeVerificationModel | None:
        row = self.db.scalar(
            self._active(vacancy_id)
            .where(ResumeVerification.score < threshold)
            .order_by(ResumeVerification.score, ResumeVerification.id)
            .limit(1)
        )
        return None if row is None else ResumeVerificationModel.model_validate(row)

    def _active(self, vacancy_id: int):
        return (
            select(ResumeVerification)
            .join(Applications, Applications.id == ResumeVerification.application_id)
            .where(
                Applications.vacancy_id == vacancy_id,
                Applications.status != "rejected",
                ResumeVerification.status == "done",
            )
        )
