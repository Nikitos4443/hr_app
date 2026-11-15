import logging
from datetime import UTC, datetime

from fastapi import HTTPException
from starlette import status

from hr_core.event_bridge import AnalyzerScheduler
from hr_core.models.user_model import User
from hr_core.models.vacancy_model import Vacancy
from hr_core.repository_interfaces.IVacanciesRepository import (
    IVacanciesRepository,
    VacancyHasDependenciesError,
)
from modules.auth.dto.principal import AuthPrincipal
from modules.companies.ICompanyService import ICompanyService
from modules.users.IUserService import IUserService
from modules.vacancies.dto.vacancy_dto import CreateVacancyDTO, UpdateVacancyDTO
from modules.vacancies.IVacancyService import IVacancyService

logger = logging.getLogger(__name__)


class VacancyService(IVacancyService):
    def __init__(
        self,
        repo: IVacanciesRepository,
        users_service: IUserService,
        companies_service: ICompanyService,
        scheduler: AnalyzerScheduler,
    ):
        self.repo = repo
        self.users_service = users_service
        self.companies_service = companies_service
        self.scheduler = scheduler

    def create_vacancy(self, actor: AuthPrincipal, dto: CreateVacancyDTO) -> Vacancy:
        user = self._load_member(actor)
        company = self.companies_service.get_by_id(user.company_id)
        if dto.deadline_at is not None:
            self._ensure_future(dto.deadline_at)
        vacancy = self.repo.create(
            Vacancy(
                **dto.model_dump(),
                company=company.name,
                company_id=company.id,
                created_by=user.id,
            )
        )
        if self._should_schedule(vacancy):
            try:
                self.scheduler.schedule(vacancy.id, self._deadline_utc(vacancy))
            except Exception as e:
                # Do not keep a vacancy that would silently never be analyzed.
                self.repo.delete(vacancy.id)
                raise self._scheduling_failed() from e
        return vacancy

    def list_vacancies(self, actor: AuthPrincipal) -> list[Vacancy]:
        user = self._load_member(actor)
        return self.repo.list_by_company(user.company_id)

    def get_vacancy(self, actor: AuthPrincipal, vacancy_id: int) -> Vacancy:
        return self._get_own(actor, vacancy_id)

    def update_vacancy(
        self, actor: AuthPrincipal, vacancy_id: int, dto: UpdateVacancyDTO
    ) -> Vacancy:
        vacancy = self._get_own(actor, vacancy_id)
        changes = dto.model_dump(exclude_unset=True)
        if changes.get("deadline_at") is not None:
            self._ensure_future(changes["deadline_at"])

        for field, value in changes.items():
            setattr(vacancy, field, value)
        if vacancy.title is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="title cannot be null"
            )
        if (
            vacancy.salary_min is not None
            and vacancy.salary_max is not None
            and vacancy.salary_min > vacancy.salary_max
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="salary_min cannot be greater than salary_max",
            )
        if "deadline_at" in changes or "status" in changes:
            self._sync_schedule(vacancy)
        return self.repo.update(vacancy)

    def delete_vacancy(self, actor: AuthPrincipal, vacancy_id: int) -> None:
        vacancy = self._get_own(actor, vacancy_id)
        try:
            self.repo.delete(vacancy.id)
        except VacancyHasDependenciesError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vacancy has applications and cannot be deleted",
            ) from e
        self._cancel_schedule(vacancy.id)

    def _load_member(self, actor: AuthPrincipal) -> User:
        user = self.users_service.get_by_id(actor.id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if user.company_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User is not attached to a company"
            )
        return user

    def _get_own(self, actor: AuthPrincipal, vacancy_id: int) -> Vacancy:
        user = self._load_member(actor)
        vacancy = self.repo.get_by_id(vacancy_id)
        if vacancy is None or vacancy.company_id != user.company_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
        return vacancy

    @staticmethod
    def _deadline_utc(vacancy: Vacancy) -> datetime | None:
        # Some backends (SQLite) drop the timezone; stored deadlines are always UTC.
        deadline = vacancy.deadline_at
        if deadline is not None and deadline.tzinfo is None:
            return deadline.replace(tzinfo=UTC)
        return deadline

    def _should_schedule(self, vacancy: Vacancy) -> bool:
        deadline = self._deadline_utc(vacancy)
        return vacancy.status == "open" and deadline is not None and deadline > datetime.now(UTC)

    @staticmethod
    def _ensure_future(deadline_at: datetime) -> None:
        if deadline_at <= datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="deadline_at must be in the future",
            )

    @staticmethod
    def _scheduling_failed() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to schedule vacancy analysis"
        )

    def _sync_schedule(self, vacancy: Vacancy) -> None:
        """Make the analyzer schedule match the vacancy: one run at the deadline while open."""
        try:
            if self._should_schedule(vacancy):
                self.scheduler.schedule(vacancy.id, self._deadline_utc(vacancy))
            else:
                self.scheduler.cancel(vacancy.id)
        except Exception as e:
            raise self._scheduling_failed() from e

    def _cancel_schedule(self, vacancy_id: int) -> None:
        # The vacancy is already gone; a leftover schedule would only fail harmlessly.
        try:
            self.scheduler.cancel(vacancy_id)
        except Exception:
            logger.exception("Failed to cancel analyzer schedule for vacancy %s", vacancy_id)
