from abc import ABC, abstractmethod

from hr_core.models.vacancy_model import Vacancy


class IVacanciesRepository(ABC):
    @abstractmethod
    def create(self, entity: Vacancy) -> Vacancy: ...

    @abstractmethod
    def get_by_id(self, vacancy_id: int) -> Vacancy | None: ...
