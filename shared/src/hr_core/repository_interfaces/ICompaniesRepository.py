from abc import ABC, abstractmethod

from hr_core.models.company_model import Company


class ICompaniesRepository(ABC):
    @abstractmethod
    def create(self, entity: Company) -> Company: ...

    @abstractmethod
    def get_by_id(self, company_id: int) -> Company | None: ...
