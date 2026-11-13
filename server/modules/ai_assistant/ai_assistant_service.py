
from abc import ABC, abstractmethod
from shared.src.hr_core.repository_interfaces.IVacanciesRepository import  IVacanciesRepository
class IAIAssitant(ABC):
    pass


class AIAssitant(IAIAssitant):
    def __init__(self, vacancy_repository : IVacanciesRepository):
        self.repo = vacancy_repository

    def get_by_id(self, id):
        return self.repo.get_by_id(id)