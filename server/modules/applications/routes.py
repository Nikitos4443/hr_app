from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from fastapi_utils.cbv import cbv
from ioc.index import get_application_management_service
from modules.applications.dto.application_dto import (
    ApplicationActionResult,
    ApplicationDetailResponse,
    ApplicationListResponse,
    ApplicationStatus,
    BulkActionDTO,
    BulkActionResponse,
)
from modules.applications.IApplicationManagementService import IApplicationManagementService
from modules.auth.guards import CurrentPrincipalDep, require_roles

from hr_core.models.user_model import UserRole

router = APIRouter(tags=["applications"])


@cbv(router)
class ApplicationsRouter:
    service: IApplicationManagementService = Depends(get_application_management_service)

    @router.get("/vacancies/{vacancy_id}/applications", response_model=ApplicationListResponse)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def list_applications(
        self,
        vacancy_id: int,
        principal: CurrentPrincipalDep,
        application_status: Annotated[ApplicationStatus | None, Query(alias="status")] = None,
        search: Annotated[str | None, Query(max_length=200)] = None,
        sort: Literal["created_at", "resume_score", "rank"] = "created_at",
        order: Literal["asc", "desc"] = "desc",
        limit: Annotated[int, Query(ge=1, le=200)] = 50,
        offset: Annotated[int, Query(ge=0)] = 0,
    ):
        return self.service.list_applications(
            principal,
            vacancy_id,
            status=application_status,
            search=search,
            sort=sort,
            descending=order == "desc",
            limit=limit,
            offset=offset,
        )

    @router.post("/vacancies/{vacancy_id}/applications/bulk", response_model=BulkActionResponse)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def bulk_action(
        self, vacancy_id: int, dto: BulkActionDTO, principal: CurrentPrincipalDep
    ):
        return self.service.bulk_action(principal, vacancy_id, dto.ids, dto.action)

    @router.get("/applications/{application_id}", response_model=ApplicationDetailResponse)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def get_application(self, application_id: int, principal: CurrentPrincipalDep):
        return self.service.get_application(principal, application_id)

    @router.post("/applications/{application_id}/invite", response_model=ApplicationActionResult)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def invite(self, application_id: int, principal: CurrentPrincipalDep):
        return self.service.invite(principal, application_id)

    @router.post("/applications/{application_id}/shortlist", response_model=ApplicationActionResult)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def shortlist(self, application_id: int, principal: CurrentPrincipalDep):
        return self.service.shortlist(principal, application_id)

    @router.post("/applications/{application_id}/reject", response_model=ApplicationActionResult)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def reject(self, application_id: int, principal: CurrentPrincipalDep):
        return self.service.reject(principal, application_id)
