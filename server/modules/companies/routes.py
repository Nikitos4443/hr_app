from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_utils.cbv import cbv
from ioc.index import get_catalog_sync, get_companies_service
from starlette import status

from hr_core.models.company_model import Company
from hr_core.models.user_model import UserRole
from modules.auth.guards import CurrentPrincipalDep, require_roles
from modules.companies.dto.company_dto import CreateCompanyDTO, UpdateCompanyDTO
from modules.companies.ICompanyService import ICompanyService
from modules.knowledge.sync import CatalogSync

router = APIRouter(prefix="/companies", tags=["companies"])


@cbv(router)
class CompaniesRouter:
    companies_service: ICompanyService = Depends(get_companies_service)
    catalog_sync: CatalogSync = Depends(get_catalog_sync)

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=Company)
    @require_roles(UserRole.COMPANY_ADMIN)
    async def create_company(
        self, principal: CurrentPrincipalDep, dto: CreateCompanyDTO, background: BackgroundTasks
    ):
        company = self.companies_service.create_company(principal, dto)
        background.add_task(self.catalog_sync.company_saved, company)
        return company

    @router.get("/{company_id}", response_model=Company)
    @require_roles(UserRole.COMPANY_ADMIN)
    async def get_company(self, company_id: int, principal: CurrentPrincipalDep):
        return self.companies_service.get_company(principal, company_id)

    @router.patch("/{company_id}", response_model=Company)
    @require_roles(UserRole.COMPANY_ADMIN)
    async def update_company(
        self,
        company_id: int,
        dto: UpdateCompanyDTO,
        principal: CurrentPrincipalDep,
        background: BackgroundTasks,
    ):
        company = self.companies_service.update_company(principal, company_id, dto)
        background.add_task(self.catalog_sync.company_saved, company)
        return company

    @router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
    @require_roles(UserRole.COMPANY_ADMIN)
    async def delete_company(
        self, company_id: int, principal: CurrentPrincipalDep, background: BackgroundTasks
    ):
        self.companies_service.delete_company(principal, company_id)
        background.add_task(self.catalog_sync.company_deleted, company_id)
