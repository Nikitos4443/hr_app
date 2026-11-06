from abc import ABC, abstractmethod

from database.models.vacancy_model import Vacancy


class IVacanciesRepository(ABC):
    @abstractmethod
    def create(self, entity: Vacancy) -> Vacancy: ...
