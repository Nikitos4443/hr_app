from abc import ABC, abstractmethod

from database.models.application_model import Application


class IApplicationsRepository(ABC):
    @abstractmethod
    def create(self, entity: Application) -> Application: ...
