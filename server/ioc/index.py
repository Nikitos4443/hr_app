from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from ioc.db_deps import (
    ApplicationsRepoDep,
    CompaniesRepoDep,
    QuestionsRepoDep,
    ResumeVerificationRepoDep,
    TextVerificationRepoDep,
    UsersRepoDep,
    VacanciesRepoDep,
    VideoVerificationRepoDep,
)
from modules.applications.ApplicationService import ApplicationsService
from modules.applications.IApplicationService import IApplicationService
from modules.auth.AuthService import AuthService
from modules.auth.IAuthService import IAuthService
from modules.companies.CompanyService import CompanyService
from modules.companies.ICompanyService import ICompanyService
from modules.flow.services.IResumeService import IResumeService
from modules.flow.services.ITextService import ITextService
from modules.flow.services.IVideoService import IVideoService
from modules.flow.services.ResumeService import ResumeService
from modules.flow.services.TextService import TextService
from modules.flow.services.VideoService import VideoService
from modules.users.IUserService import IUserService
from modules.users.UserService import UserService
from modules.vacancies.IVacancyService import IVacancyService
from modules.vacancies.VacancyService import VacancyService

from config import settings
from hr_core.event_bridge import AnalyzerScheduler
from hr_core.s3.service import S3Service


def get_users_service(repo: UsersRepoDep) -> IUserService:
    return UserService(repo=repo)


UsersServiceDep = Annotated[IUserService, Depends(get_users_service)]


def get_companies_service(
    repo: CompaniesRepoDep, users_service: UsersServiceDep
) -> ICompanyService:
    return CompanyService(repo=repo, users_service=users_service)


CompaniesServiceDep = Annotated[ICompanyService, Depends(get_companies_service)]


@lru_cache
def get_analyzer_scheduler() -> AnalyzerScheduler:
    return AnalyzerScheduler(
        lambda_arn=settings.analyzer_lambda_arn,
        role_arn=settings.analyzer_scheduler_role_arn,
    )


AnalyzerSchedulerDep = Annotated[AnalyzerScheduler, Depends(get_analyzer_scheduler)]


def get_vacancies_service(
    repo: VacanciesRepoDep,
    users_service: UsersServiceDep,
    companies_service: CompaniesServiceDep,
    scheduler: AnalyzerSchedulerDep,
) -> IVacancyService:
    return VacancyService(
        repo=repo,
        users_service=users_service,
        companies_service=companies_service,
        scheduler=scheduler,
    )


def get_auth_service(users_service: UsersServiceDep) -> IAuthService:
    return AuthService(users_service=users_service)


def get_resume_service(repo: ResumeVerificationRepoDep) -> IResumeService:
    return ResumeService(repo=repo)


def get_s3_service() -> S3Service:
    return S3Service()


def get_applications_service(repo: ApplicationsRepoDep) -> IApplicationService:
    return ApplicationsService(repo)


ApplicationsServiceDep = Annotated[IApplicationService, Depends(get_applications_service)]


def get_video_service(
    videos: VideoVerificationRepoDep,
    questions: QuestionsRepoDep,
    resumes: ResumeVerificationRepoDep,
) -> IVideoService:
    return VideoService(videos=videos, questions=questions, resumes=resumes)


def get_text_service(
    texts: TextVerificationRepoDep,
    questions: QuestionsRepoDep,
    resumes: ResumeVerificationRepoDep,
) -> ITextService:
    return TextService(texts=texts, questions=questions, resumes=resumes)
