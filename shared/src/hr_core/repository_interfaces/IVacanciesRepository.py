from abc import ABC, abstractmethod

from hr_core.models.vacancy_model import Vacancy


class VacancyHasDependenciesError(Exception):
    """The vacancy is still referenced by other records (e.g. applications)."""


class IVacanciesRepository(ABC):
    @abstractmethod
    def create(self, entity: Vacancy) -> Vacancy: ...

    @abstractmethod
    def get_by_id(self, vacancy_id: int) -> Vacancy | None: ...

    @abstractmethod
    def list_by_company(self, company_id: int) -> list[Vacancy]: ...

    @abstractmethod
    def update(self, entity: Vacancy) -> Vacancy: ...

    @abstractmethod
    def delete(self, vacancy_id: int) -> None: ...

    @abstractmethod
    def update_selection_status(self, vacancy_id: int, status: str) -> None: ...
