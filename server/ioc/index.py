from typing import Annotated

from fastapi import Depends
from ioc.db_deps import (
    ApplicationsRepoDep,
    QuestionsRepoDep,
    ResumeVerificationRepoDep,
    TextVerificationRepoDep,
    UsersRepoDep,
    VideoVerificationRepoDep,
)
from modules.applications.ApplicationService import ApplicationsService
from modules.applications.IApplicationService import IApplicationService
from modules.auth.AuthService import AuthService
from modules.auth.IAuthService import IAuthService
from modules.flow.services.IResumeService import IResumeService
from modules.flow.services.ITextService import ITextService
from modules.flow.services.IVideoService import IVideoService
from modules.flow.services.ResumeService import ResumeService
from modules.flow.services.TextService import TextService
from modules.flow.services.VideoService import VideoService

from hr_core.s3.service import S3Service


def get_auth_service(repo: UsersRepoDep) -> IAuthService:
    return AuthService(repo=repo)


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
