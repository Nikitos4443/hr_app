from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from hr_core.models.application_model import Application
from hr_core.repository_interfaces.IApplicationsRepository import IApplicationsRepository
from hr_core.sql.tables.applications import Applications


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

    def update_status(self, application_id: int, status: str) -> Application | None:
        row = self.db.get(Applications, application_id)
        if row is None:
            return None
        row.status = status
        self.db.commit()
        self.db.refresh(row)
        return Application.model_validate(row)

    def get_rejected_not_notified(self, vacancy_id: int) -> list[Application]:
        rows = self.db.scalars(
            select(Applications).where(
                Applications.vacancy_id == vacancy_id,
                Applications.status == "rejected",
                Applications.rejection_notified_at.is_(None),
            )
        )
        return [Application.model_validate(row) for row in rows]

    def mark_rejection_notified(self, application_id: int) -> None:
        row = self.db.get(Applications, application_id)
        row.rejection_notified_at = datetime.now(UTC)
        self.db.commit()
