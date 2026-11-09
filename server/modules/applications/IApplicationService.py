from abc import ABC, abstractmethod

from fastapi import UploadFile

from modules.applications.dto.create_application_dto import CreateApplicationDTO


class IApplicationService(ABC):
    @abstractmethod
    async def create_application(self, dto: CreateApplicationDTO): ...