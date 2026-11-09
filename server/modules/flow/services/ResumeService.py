from fastapi import UploadFile
from fastapi.security import OAuth2PasswordBearer

from hr_core.repository_interfaces.IUsersRepository import IUsersRepository
from modules.flow.services.IResumeService import IResumeService


class ResumeService(IResumeService):
    def __init__(self, repo: IUsersRepository):
        self.repo = repo

    async def load_resume(self, file: UploadFile):
        pass
