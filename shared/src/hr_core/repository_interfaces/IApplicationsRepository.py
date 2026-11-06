from abc import ABC, abstractmethod

from hr_core.models.application_model import Application


class IApplicationsRepository(ABC):
    @abstractmethod
    def create(self, entity: Application) -> Application: ...
