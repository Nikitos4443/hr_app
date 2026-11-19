from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from ioc.db_deps import (
    ApplicationsRepoDep,
    CompaniesRepoDep,
    EvaluationsRepoDep,
    QuestionsRepoDep,
    ResumeVerificationRepoDep,
    TextVerificationRepoDep,
    UsersRepoDep,
    VacanciesRepoDep,
    VideoVerificationRepoDep,
)
from modules.applications.ApplicationManagementService import ApplicationManagementService
from modules.applications.ApplicationService import ApplicationsService
from modules.applications.IApplicationManagementService import IApplicationManagementService
from modules.applications.IApplicationService import IApplicationService
from modules.auth.AuthService import AuthService
from modules.auth.IAuthService import IAuthService
from modules.companies.CompanyService import CompanyService
from modules.companies.ICompanyService import ICompanyService
from modules.flow.services.IResumeService import IResumeService
from modules.flow.services.ITextService import ITextService
from modules.flow.services.IVideoService import IVideoService
from modules.flow.services.ResumeService import ResumeService
from modules.flow.services.ScreeningService import ScreeningService
from modules.flow.services.TextService import TextService
from modules.flow.services.VideoService import VideoService
from modules.questions.IQuestionService import IQuestionService
from modules.questions.QuestionService import QuestionService
from modules.users.IUserService import IUserService
from modules.users.UserService import UserService
from modules.vacancies.IVacancyService import IVacancyService
from modules.vacancies.VacancyService import VacancyService

from config import BUCKET_NAME, settings
from hr_core.event_bridge import AnalyzerScheduler
from hr_core.notifications.EmailNotificationChannel import EmailNotificationChannel
from hr_core.notifications.INotificationChannel import INotificationChannel
from hr_core.s3.service import S3Service
from hr_core.services.CandidateCleanupService import CandidateCleanupService


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
    applications: ApplicationsRepoDep,
    questions: QuestionsRepoDep,
) -> IVacancyService:
    return VacancyService(
        applications=applications,
        questions=questions,
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


def get_applications_service(
    repo: ApplicationsRepoDep, vacancies: VacanciesRepoDep
) -> IApplicationService:
    return ApplicationsService(repo, vacancies)


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


def get_screening_service(
    vacancies: VacanciesRepoDep,
    questions: QuestionsRepoDep,
    resumes: ResumeVerificationRepoDep,
    texts: TextVerificationRepoDep,
    videos: VideoVerificationRepoDep,
) -> ScreeningService:
    return ScreeningService(
        vacancies=vacancies, questions=questions, resumes=resumes, texts=texts, videos=videos
    )


def get_question_service(
    repo: QuestionsRepoDep,
    vacancies_service: Annotated[IVacancyService, Depends(get_vacancies_service)],
) -> IQuestionService:
    return QuestionService(repo=repo, vacancies_service=vacancies_service)


@lru_cache
def get_notification_channel() -> INotificationChannel:
    return EmailNotificationChannel(settings.gmail_user, settings.gmail_app_password)


def get_application_management_service(
    vacancies_service: Annotated[IVacancyService, Depends(get_vacancies_service)],
    applications: ApplicationsRepoDep,
    resumes: ResumeVerificationRepoDep,
    questions: QuestionsRepoDep,
    texts: TextVerificationRepoDep,
    videos: VideoVerificationRepoDep,
    evaluations: EvaluationsRepoDep,
    s3: Annotated[S3Service, Depends(get_s3_service)],
    channel: Annotated[INotificationChannel, Depends(get_notification_channel)],
) -> IApplicationManagementService:
    cleanup = CandidateCleanupService(
        applications=applications,
        resumes=resumes,
        videos=videos,
        texts=texts,
        evaluations=evaluations,
        s3=s3,
        bucket_name=BUCKET_NAME,
    )
    return ApplicationManagementService(
        vacancies_service=vacancies_service,
        applications=applications,
        resumes=resumes,
        questions=questions,
        texts=texts,
        videos=videos,
        evaluations=evaluations,
        cleanup=cleanup,
        s3=s3,
        bucket_name=BUCKET_NAME,
        channel=channel,
        frontend_url=settings.frontend_url,
    )
