from abc import ABC, abstractmethod

from hr_core.models.company_model import Company
from modules.auth.dto.principal import AuthPrincipal
from modules.companies.dto.company_dto import CreateCompanyDTO, UpdateCompanyDTO


class ICompanyService(ABC):
    @abstractmethod
    def get_by_id(self, company_id: int) -> Company | None: ...

    @abstractmethod
    def create_company(self, actor: AuthPrincipal, dto: CreateCompanyDTO) -> Company: ...

    @abstractmethod
    def get_company(self, actor: AuthPrincipal, company_id: int) -> Company: ...

    @abstractmethod
    def update_company(
        self, actor: AuthPrincipal, company_id: int, dto: UpdateCompanyDTO
    ) -> Company: ...

    @abstractmethod
    def delete_company(self, actor: AuthPrincipal, company_id: int) -> None: ...
