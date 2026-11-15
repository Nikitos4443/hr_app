from datetime import UTC, datetime
from typing import Any

from sqlalchemy import delete, select
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
        self, application_id: int, score: float, llm_review: dict[str, Any]
    ) -> ResumeVerificationModel:
        row = self.db.scalar(
            select(ResumeVerification).where(ResumeVerification.application_id == application_id)
        )
        if row is None:
            row = ResumeVerification(application_id=application_id)
            self.db.add(row)
        row.score = score
        row.llm_review = llm_review
        row.status = "done"
        row.processed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(row)
        return ResumeVerificationModel.model_validate(row)

    def get_active_scores(self, vacancy_id: int) -> dict[int, float]:
        rows = self.db.execute(
            select(ResumeVerification.application_id, ResumeVerification.score)
            .join(Applications, Applications.id == ResumeVerification.application_id)
            .where(
                Applications.vacancy_id == vacancy_id,
                Applications.status != "rejected",
                ResumeVerification.status == "done",
            )
        )
        return {application_id: score for application_id, score in rows}

    def get_by_application(self, application_id: int) -> ResumeVerificationModel | None:
        row = self.db.scalar(
            select(ResumeVerification).where(ResumeVerification.application_id == application_id)
        )
        return None if row is None else ResumeVerificationModel.model_validate(row)

    def delete_by_application(self, application_id: int) -> None:
        self.db.execute(
            delete(ResumeVerification).where(ResumeVerification.application_id == application_id)
        )
        self.db.commit()

    def list_done_by_vacancy(self, vacancy_id: int) -> list[ResumeVerificationModel]:
        rows = self.db.scalars(
            select(ResumeVerification)
            .join(Applications, Applications.id == ResumeVerification.application_id)
            .where(
                Applications.vacancy_id == vacancy_id,
                Applications.status != "rejected",
                ResumeVerification.status == "done",
            )
        )
        return [ResumeVerificationModel.model_validate(row) for row in rows]
