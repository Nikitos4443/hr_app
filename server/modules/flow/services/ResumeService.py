from fastapi import UploadFile
from modules.flow.services.IResumeService import IResumeService

from hr_core.repository_interfaces.IUsersRepository import IUsersRepository


class ResumeService(IResumeService):
    def __init__(self, repo: IUsersRepository):
        self.repo = repo

    async def load_resume(self, file: UploadFile):
        pass
