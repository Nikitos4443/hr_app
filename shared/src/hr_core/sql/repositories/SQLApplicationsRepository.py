from datetime import UTC, datetime

from sqlalchemy import case, delete, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hr_core.models.application_model import Application, ApplicationSummary
from hr_core.repository_interfaces.IApplicationsRepository import (
    DuplicateApplicationError,
    IApplicationsRepository,
)
from hr_core.sql.tables.applications import Applications
from hr_core.sql.tables.evaluations import Evaluations
from hr_core.sql.tables.resume_verification import ResumeVerification
from hr_core.sql.tables.text_verification import TextVerification
from hr_core.sql.tables.video_verification import VideoVerification

# Status shown to staff: "invited" is derived from screening_invited_at, not stored.
_DERIVED_STATUS = case(
    (Applications.status == "rejected", "rejected"),
    (Applications.status == "shortlisted", "shortlisted"),
    (Applications.screening_invited_at.is_not(None), "invited"),
    else_="pending",
)


class SQLApplicationsRepository(IApplicationsRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create(self, entity: Application) -> Application:
        row = Applications(**entity.model_dump(exclude={"id"}, exclude_none=True))
        self.db.add(row)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise DuplicateApplicationError from e
        self.db.refresh(row)
        return Application.model_validate(row)

    def get_by_vacancy_and_email(self, vacancy_id: int, email: str) -> Application | None:
        row = self.db.scalar(
            select(Applications).where(
                Applications.vacancy_id == vacancy_id, Applications.email == email
            )
        )
        return None if row is None else Application.model_validate(row)

    def delete(self, application_id: int) -> None:
        self.db.execute(delete(Applications).where(Applications.id == application_id))
        self.db.commit()

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
        if row.status != status:
            row.status = status
            row.status_changed_at = datetime.now(UTC)
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

    def list_summaries(
        self,
        vacancy_id: int,
        *,
        status: str | None,
        search: str | None,
        sort: str,
        descending: bool,
        limit: int,
        offset: int,
    ) -> tuple[list[ApplicationSummary], int]:
        answered = (
            select(func.count())
            .where(TextVerification.application_id == Applications.id)
            .where(TextVerification.status == "done")
            .correlate(Applications)
            .scalar_subquery()
            + select(func.count())
            .where(VideoVerification.application_id == Applications.id)
            .where(VideoVerification.status == "done")
            .correlate(Applications)
            .scalar_subquery()
        )
        base = (
            select(Applications.id)
            .outerjoin(ResumeVerification, ResumeVerification.application_id == Applications.id)
            .outerjoin(Evaluations, Evaluations.application_id == Applications.id)
            .where(Applications.vacancy_id == vacancy_id)
        )
        if status is not None:
            base = base.where(status == _DERIVED_STATUS)
        if search:
            escaped = search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            pattern = f"%{escaped}%"
            base = base.where(
                or_(
                    Applications.email.ilike(pattern, escape="\\"),
                    Applications.full_name.ilike(pattern, escape="\\"),
                )
            )
        total = self.db.scalar(select(func.count()).select_from(base.subquery())) or 0

        sort_columns = {
            "created_at": Applications.created_at,
            "resume_score": ResumeVerification.score,
            "rank": Evaluations.order,
        }
        column = sort_columns[sort]
        ordering = column.desc() if descending else column.asc()
        query = (
            select(
                Applications,
                _DERIVED_STATUS.label("derived_status"),
                ResumeVerification.status.label("resume_status"),
                ResumeVerification.score.label("resume_score"),
                answered.label("answered_count"),
                Evaluations.order.label("rank"),
                Evaluations.summary.label("ai_summary"),
            )
            .outerjoin(ResumeVerification, ResumeVerification.application_id == Applications.id)
            .outerjoin(Evaluations, Evaluations.application_id == Applications.id)
            .where(Applications.id.in_(base.with_only_columns(Applications.id)))
            .order_by(ordering.nulls_last(), Applications.id)
            .limit(limit)
            .offset(offset)
        )
        items = [
            ApplicationSummary(
                id=row.Applications.id,
                email=row.Applications.email,
                full_name=row.Applications.full_name,
                status=row.derived_status,
                created_at=row.Applications.created_at,
                resume_status=row.resume_status,
                resume_score=row.resume_score,
                screening_invited_at=row.Applications.screening_invited_at,
                answered_count=row.answered_count or 0,
                rank=row.rank,
                ai_summary=row.ai_summary,
            )
            for row in self.db.execute(query)
        ]
        return items, total

    def count_by_status(self, vacancy_id: int) -> dict[str, int]:
        rows = self.db.execute(
            select(_DERIVED_STATUS, func.count())
            .where(Applications.vacancy_id == vacancy_id)
            .group_by(_DERIVED_STATUS)
        )
        return dict(rows.all())

    def count_by_vacancies(self, vacancy_ids: list[int]) -> dict[int, int]:
        if not vacancy_ids:
            return {}
        rows = self.db.execute(
            select(Applications.vacancy_id, func.count())
            .where(Applications.vacancy_id.in_(vacancy_ids))
            .group_by(Applications.vacancy_id)
        )
        return dict(rows.all())

    def _list(self, query) -> list[Application]:
        return [Application.model_validate(row) for row in self.db.scalars(query)]
