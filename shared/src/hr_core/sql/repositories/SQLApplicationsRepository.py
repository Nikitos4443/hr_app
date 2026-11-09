from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from hr_core.models.application_model import Application
from hr_core.repository_interfaces.IApplicationsRepository import IApplicationsRepository
from hr_core.sql.tables.applications import Applications
from hr_core.sql.tables.resume_verification import ResumeVerification


class SQLApplicationsRepository(IApplicationsRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: Application) -> Application:
        row = Applications(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return Application.model_validate(row)

    def get_by_id(self, application_id: int) -> Application | None:
        row = self.db.get(Applications, application_id)
        return None if row is None else Application.model_validate(row)

    def get_by_screening_token(self, token: str) -> Application | None:
        row = self.db.scalar(select(Applications).where(Applications.screening_token == token))
        return None if row is None else Application.model_validate(row)

    def update_status(self, application_id: int, status: str) -> Application | None:
        row = self.db.get(Applications, application_id)
        if row is None:
            return None
        row.status = status
        self.db.commit()
        self.db.refresh(row)
        return Application.model_validate(row)

    def get_not_invited(self, vacancy_id: int) -> list[Application]:
        return self._list(
            select(Applications)
            .join(ResumeVerification, ResumeVerification.application_id == Applications.id)
            .where(
                Applications.vacancy_id == vacancy_id,
                Applications.status != "rejected",
                Applications.screening_invited_at.is_(None),
                ResumeVerification.status == "done",
            )
        )

    def mark_screening_invited(self, application_id: int) -> None:
        row = self.db.get(Applications, application_id)
        row.screening_invited_at = datetime.now(UTC)
        self.db.commit()

    def get_rejected_not_purged(self, vacancy_id: int) -> list[Application]:
        return self._list(
            select(Applications).where(
                Applications.vacancy_id == vacancy_id,
                Applications.status == "rejected",
                Applications.purged_at.is_(None),
            )
        )

    def mark_purged(self, application_id: int) -> None:
        row = self.db.get(Applications, application_id)
        row.full_name = None
        row.purged_at = datetime.now(UTC)
        self.db.commit()

    def get_rejected_not_notified(self, vacancy_id: int) -> list[Application]:
        return self._list(
            select(Applications).where(
                Applications.vacancy_id == vacancy_id,
                Applications.status == "rejected",
                Applications.rejection_notified_at.is_(None),
            )
        )

    def mark_rejection_notified(self, application_id: int) -> None:
        row = self.db.get(Applications, application_id)
        row.rejection_notified_at = datetime.now(UTC)
        self.db.commit()

    def _list(self, query) -> list[Application]:
        return [Application.model_validate(row) for row in self.db.scalars(query)]
