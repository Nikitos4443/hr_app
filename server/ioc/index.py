from typing import Annotated

from fastapi import Depends
from ioc.db_deps import ApplicationsRepoDep, UsersRepoDep
from modules.applications.ApplicationService import ApplicationsService
from modules.applications.IApplicationService import IApplicationService
from modules.auth.AuthService import AuthService
from modules.auth.IAuthService import IAuthService
from modules.flow.services.IResumeService import IResumeService
from modules.flow.services.ResumeService import ResumeService

from hr_core.s3.service import S3Service


def get_auth_service(repo: UsersRepoDep) -> IAuthService:
    return AuthService(repo=repo)


AuthServiceDep = Annotated[IAuthService, Depends(get_auth_service)]


def get_resume_service(repo: UsersRepoDep) -> IResumeService:
    return ResumeService(repo=repo)


ResumeServiceDep = Annotated[IResumeService, Depends(get_resume_service)]


def get_s3_service() -> S3Service:
    return S3Service()


S3ServiceDep = Annotated[S3Service, Depends(get_s3_service)]


def get_applications_service(repo: ApplicationsRepoDep) -> IApplicationService:
    return ApplicationsService(repo)


ApplicationsServiceDep = Annotated[IApplicationService, Depends(get_applications_service)]
