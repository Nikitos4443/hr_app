from datetime import UTC, datetime

from fastapi import HTTPException
from modules.applications.dto.create_application_dto import CreateApplicationDTO
from modules.applications.IApplicationService import IApplicationService
from starlette import status

from hr_core.models.application_model import Application
from hr_core.repository_interfaces.IApplicationsRepository import (
    DuplicateApplicationError,
    IApplicationsRepository,
)
from hr_core.repository_interfaces.IVacanciesRepository import IVacanciesRepository


class ApplicationsService(IApplicationService):
    def __init__(self, repo: IApplicationsRepository, vacancies: IVacanciesRepository):
        self.repo = repo
        self.vacancies = vacancies

    async def create_application(self, dto: CreateApplicationDTO):
        vacancy = self.vacancies.get_by_id(dto.vacancy_id)
        if vacancy is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
        if vacancy.status != "open":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Vacancy is closed for applications"
            )
        deadline = vacancy.deadline_utc()
        if deadline is not None and deadline <= datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The application deadline for this vacancy has passed",
            )
        already_applied = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied to this vacancy",
        )
        if self.repo.get_by_vacancy_and_email(dto.vacancy_id, dto.email) is not None:
            raise already_applied

        try:
            return self.repo.create(
                Application(
                    email=dto.email,
                    full_name=dto.full_name,
                    vacancy_id=dto.vacancy_id,
                    status="pending",
                )
            )
        except DuplicateApplicationError as e:
            raise already_applied from e

    async def get_by_screening_token(self, token: str) -> Application | None:
        return self.repo.get_by_screening_token(token)

    async def delete_application(self, application_id: int) -> None:
        self.repo.delete(application_id)
