from abc import ABC, abstractmethod

from hr_core.models.vacancy_model import Vacancy
from modules.auth.dto.principal import AuthPrincipal
from modules.vacancies.dto.vacancy_dto import CreateVacancyDTO, UpdateVacancyDTO


class IVacancyService(ABC):
    @abstractmethod
    def create_vacancy(self, actor: AuthPrincipal, dto: CreateVacancyDTO) -> Vacancy: ...

    @abstractmethod
    def list_vacancies(self, actor: AuthPrincipal) -> list[Vacancy]: ...

    @abstractmethod
    def get_vacancy(self, actor: AuthPrincipal, vacancy_id: int) -> Vacancy: ...

    @abstractmethod
    def update_vacancy(
        self, actor: AuthPrincipal, vacancy_id: int, dto: UpdateVacancyDTO
    ) -> Vacancy: ...

    @abstractmethod
    def delete_vacancy(self, actor: AuthPrincipal, vacancy_id: int) -> None: ...
