from abc import ABC, abstractmethod

from fastapi import UploadFile


class IResumeService(ABC):
    @abstractmethod
    async def load_resume(self, file: UploadFile): ...
