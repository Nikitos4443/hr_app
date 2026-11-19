from abc import ABC, abstractmethod

from hr_core.models.application_model import Application, ApplicationSummary

APPLICATION_STATUSES = ("pending", "invited", "shortlisted", "rejected")


class DuplicateApplicationError(Exception):
    """The email already applied to this vacancy."""


class IApplicationsRepository(ABC):
    @abstractmethod
    def create(self, entity: Application) -> Application: ...

    @abstractmethod
    def get_by_id(self, application_id: int) -> Application | None: ...

    @abstractmethod
    def get_by_screening_token(self, token: str) -> Application | None: ...

    @abstractmethod
    def update_status(self, application_id: int, status: str) -> Application | None: ...

    @abstractmethod
    def get_not_invited(self, vacancy_id: int) -> list[Application]: ...

    @abstractmethod
    def mark_screening_invited(self, application_id: int) -> None: ...

    @abstractmethod
    def get_rejected_not_purged(self, vacancy_id: int) -> list[Application]: ...

    @abstractmethod
    def mark_purged(self, application_id: int) -> None: ...

    @abstractmethod
    def get_rejected_not_notified(self, vacancy_id: int) -> list[Application]: ...

    @abstractmethod
    def mark_rejection_notified(self, application_id: int) -> None: ...

    @abstractmethod
    def get_by_vacancy_and_email(self, vacancy_id: int, email: str) -> Application | None: ...

    @abstractmethod
    def delete(self, application_id: int) -> None: ...

    @abstractmethod
    def list_summaries(
        self,
        vacancy_id: int,
        *,
        status: str | None,
        search: str | None,
        sort: str,
        descending: bool,
        limit: int,
        offset: int,
    ) -> tuple[list[ApplicationSummary], int]:
        """Page of applications with resume/ranking data in one query, plus the filtered total."""

    @abstractmethod
    def count_by_status(self, vacancy_id: int) -> dict[str, int]:
        """Counts per derived status (pending|invited|shortlisted|rejected) for the vacancy."""

    @abstractmethod
    def count_by_vacancies(self, vacancy_ids: list[int]) -> dict[int, int]: ...
