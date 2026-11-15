from abc import ABC, abstractmethod

from hr_core.models.company_model import Company


class CompanyHasDependenciesError(Exception):
    """The company is still referenced by other records (e.g. vacancies)."""


class ICompaniesRepository(ABC):
    @abstractmethod
    def create(self, entity: Company) -> Company: ...

    @abstractmethod
    def get_by_id(self, company_id: int) -> Company | None: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Company | None: ...

    @abstractmethod
    def update(self, entity: Company) -> Company: ...

    @abstractmethod
    def delete(self, company_id: int) -> None:
        """Delete the company and detach its users from it, atomically."""
