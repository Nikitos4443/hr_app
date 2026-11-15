from fastapi import HTTPException
from starlette import status

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


class VacancyService(IVacancyService):
    def __init__(
        self,
        repo: IVacanciesRepository,
        users_service: IUserService,
        companies_service: ICompanyService,
    ):
        self.repo = repo
        self.users_service = users_service
        self.companies_service = companies_service

    def create_vacancy(self, actor: AuthPrincipal, dto: CreateVacancyDTO) -> Vacancy:
        user = self._load_member(actor)
        company = self.companies_service.get_by_id(user.company_id)
        return self.repo.create(
            Vacancy(
                **dto.model_dump(),
                company=company.name,
                company_id=company.id,
                created_by=user.id,
            )
        )

    def list_vacancies(self, actor: AuthPrincipal) -> list[Vacancy]:
        user = self._load_member(actor)
        return self.repo.list_by_company(user.company_id)

    def get_vacancy(self, actor: AuthPrincipal, vacancy_id: int) -> Vacancy:
        return self._get_own(actor, vacancy_id)

    def update_vacancy(
        self, actor: AuthPrincipal, vacancy_id: int, dto: UpdateVacancyDTO
    ) -> Vacancy:
        vacancy = self._get_own(actor, vacancy_id)

        for field, value in dto.model_dump(exclude_unset=True).items():
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
