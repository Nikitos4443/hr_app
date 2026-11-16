from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_utils.cbv import cbv
from ioc.index import get_catalog_sync, get_vacancies_service
from starlette import status

from hr_core.models.user_model import UserRole
from hr_core.models.vacancy_model import Vacancy
from modules.auth.guards import CurrentPrincipalDep, require_roles
from modules.knowledge.sync import CatalogSync
from modules.vacancies.dto.vacancy_dto import CreateVacancyDTO, UpdateVacancyDTO
from modules.vacancies.IVacancyService import IVacancyService

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@cbv(router)
class VacanciesRouter:
    vacancies_service: IVacancyService = Depends(get_vacancies_service)
    catalog_sync: CatalogSync = Depends(get_catalog_sync)

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=Vacancy)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def create_vacancy(
        self, principal: CurrentPrincipalDep, dto: CreateVacancyDTO, background: BackgroundTasks
    ):
        vacancy = self.vacancies_service.create_vacancy(principal, dto)
        background.add_task(self.catalog_sync.vacancy_saved, vacancy)
        return vacancy

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
        self,
        vacancy_id: int,
        dto: UpdateVacancyDTO,
        principal: CurrentPrincipalDep,
        background: BackgroundTasks,
    ):
        vacancy = self.vacancies_service.update_vacancy(principal, vacancy_id, dto)
        background.add_task(self.catalog_sync.vacancy_saved, vacancy)
        return vacancy

    @router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def delete_vacancy(
        self, vacancy_id: int, principal: CurrentPrincipalDep, background: BackgroundTasks
    ):
        self.vacancies_service.delete_vacancy(principal, vacancy_id)
        background.add_task(self.catalog_sync.vacancy_deleted, vacancy_id)
