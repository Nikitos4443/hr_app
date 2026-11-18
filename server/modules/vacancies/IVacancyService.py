from abc import ABC, abstractmethod

from modules.auth.dto.principal import AuthPrincipal
from modules.vacancies.dto.vacancy_dto import (
    CreateVacancyDTO,
    PublicVacancyResponse,
    UpdateVacancyDTO,
    VacancyResponse,
)


class IVacancyService(ABC):
    @abstractmethod
    def create_vacancy(self, actor: AuthPrincipal, dto: CreateVacancyDTO) -> VacancyResponse: ...

    @abstractmethod
    def list_vacancies(self, actor: AuthPrincipal) -> list[VacancyResponse]: ...

    @abstractmethod
    def get_vacancy(self, actor: AuthPrincipal, vacancy_id: int) -> VacancyResponse: ...

    @abstractmethod
    def update_vacancy(
        self, actor: AuthPrincipal, vacancy_id: int, dto: UpdateVacancyDTO
    ) -> VacancyResponse: ...

    @abstractmethod
    def delete_vacancy(self, actor: AuthPrincipal, vacancy_id: int) -> None: ...

    @abstractmethod
    def get_public(self, vacancy_id: int) -> PublicVacancyResponse: ...

    @abstractmethod
    def retry_selection(self, actor: AuthPrincipal, vacancy_id: int) -> VacancyResponse: ...
