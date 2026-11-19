from abc import ABC, abstractmethod

from modules.applications.dto.create_application_dto import CreateApplicationDTO

from hr_core.models.application_model import Application


class IApplicationService(ABC):
    @abstractmethod
    async def create_application(self, dto: CreateApplicationDTO): ...

    @abstractmethod
    async def get_by_screening_token(self, token: str) -> Application | None: ...

    @abstractmethod
    async def delete_application(self, application_id: int) -> None:
        """Roll back an application whose resume upload could not be prepared."""
