from hr_core.repository_interfaces.IApplicationsRepository import IApplicationsRepository
from hr_core.repository_interfaces.IEvaluationsRepository import IEvaluationsRepository
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from hr_core.repository_interfaces.ITextVerificationRepository import (
    ITextVerificationRepository,
)
from hr_core.repository_interfaces.IVideoVerificationRepository import (
    IVideoVerificationRepository,
)
from hr_core.s3.service import S3Service


class CandidateCleanupService:
    def __init__(
        self,
        applications: IApplicationsRepository,
        resumes: IResumeVerificationRepository,
        videos: IVideoVerificationRepository,
        texts: ITextVerificationRepository,
        evaluations: IEvaluationsRepository,
        s3: S3Service,
        bucket_name: str,
    ):
        self.applications = applications
        self.resumes = resumes
        self.videos = videos
        self.texts = texts
        self.evaluations = evaluations
        self.s3 = s3
        self.bucket_name = bucket_name

    def purge(self, application_id: int) -> None:
        resume = self.resumes.get_by_application(application_id)
        keys = [video.s3_key for video in self.videos.list_by_application(application_id)]
        if resume is not None:
            keys.append(resume.s3_key)
        self.s3.delete_objects(self.bucket_name, [key for key in keys if key])

        self.videos.delete_by_application(application_id)
        self.texts.delete_by_application(application_id)
        self.evaluations.delete_by_application(application_id)
        self.resumes.delete_by_application(application_id)
        self.applications.mark_purged(application_id)
