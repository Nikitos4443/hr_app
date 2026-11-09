from abc import ABC, abstractmethod

from hr_core.models.application_model import Application


class IApplicationsRepository(ABC):
    @abstractmethod
    def create(self, entity: Application) -> Application: ...

    @abstractmethod
    def get_by_id(self, application_id: int) -> Application | None: ...

    @abstractmethod
    def update_status(self, application_id: int, status: str) -> Application | None: ...

    @abstractmethod
    def get_rejected_not_notified(self, vacancy_id: int) -> list[Application]: ...

    @abstractmethod
    def mark_rejection_notified(self, application_id: int) -> None: ...
