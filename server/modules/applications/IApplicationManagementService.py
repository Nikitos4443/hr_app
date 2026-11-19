from abc import ABC, abstractmethod

from modules.applications.dto.application_dto import (
    ApplicationActionResult,
    ApplicationDetailResponse,
    ApplicationListResponse,
    BulkActionResponse,
)
from modules.auth.dto.principal import AuthPrincipal


class IApplicationManagementService(ABC):
    @abstractmethod
    def list_applications(
        self,
        actor: AuthPrincipal,
        vacancy_id: int,
        *,
        status: str | None,
        search: str | None,
        sort: str,
        descending: bool,
        limit: int,
        offset: int,
    ) -> ApplicationListResponse: ...

    @abstractmethod
    def get_application(
        self, actor: AuthPrincipal, application_id: int
    ) -> ApplicationDetailResponse: ...

    @abstractmethod
    def invite(self, actor: AuthPrincipal, application_id: int) -> ApplicationActionResult: ...

    @abstractmethod
    def shortlist(self, actor: AuthPrincipal, application_id: int) -> ApplicationActionResult: ...

    @abstractmethod
    def reject(self, actor: AuthPrincipal, application_id: int) -> ApplicationActionResult: ...

    @abstractmethod
    def bulk_action(
        self, actor: AuthPrincipal, vacancy_id: int, ids: list[int], action: str
    ) -> BulkActionResponse: ...
