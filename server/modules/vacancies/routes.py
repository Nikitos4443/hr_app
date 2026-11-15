from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from ioc.index import get_vacancies_service
from starlette import status

from hr_core.models.user_model import UserRole
from hr_core.models.vacancy_model import Vacancy
from modules.auth.guards import CurrentPrincipalDep, require_roles
from modules.vacancies.dto.vacancy_dto import CreateVacancyDTO, UpdateVacancyDTO
from modules.vacancies.IVacancyService import IVacancyService

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@cbv(router)
class VacanciesRouter:
    vacancies_service: IVacancyService = Depends(get_vacancies_service)

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=Vacancy)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def create_vacancy(self, principal: CurrentPrincipalDep, dto: CreateVacancyDTO):
        return self.vacancies_service.create_vacancy(principal, dto)

    @router.get("/", response_model=list[Vacancy])
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def list_vacancies(self, principal: CurrentPrincipalDep):
        return self.vacancies_service.list_vacancies(principal)

    @router.get("/{vacancy_id}", response_model=Vacancy)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def get_vacancy(self, vacancy_id: int, principal: CurrentPrincipalDep):
        return self.vacancies_service.get_vacancy(principal, vacancy_id)

    @router.patch("/{vacancy_id}", response_model=Vacancy)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def update_vacancy(
        self, vacancy_id: int, dto: UpdateVacancyDTO, principal: CurrentPrincipalDep
    ):
        return self.vacancies_service.update_vacancy(principal, vacancy_id, dto)

    @router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def delete_vacancy(self, vacancy_id: int, principal: CurrentPrincipalDep):
        self.vacancies_service.delete_vacancy(principal, vacancy_id)
