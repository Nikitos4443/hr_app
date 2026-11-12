from hr_core.models.application_model import Application
from hr_core.models.video_verification_model import VideoVerification
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from hr_core.repository_interfaces.IVideoVerificationRepository import (
    IVideoVerificationRepository,
)
from modules.flow.errors import VideoFlowError
from modules.flow.services.IVideoService import IVideoService


class VideoService(IVideoService):
    def __init__(
        self,
        videos: IVideoVerificationRepository,
        questions: IQuestionsRepository,
        resumes: IResumeVerificationRepository,
    ):
        self.videos = videos
        self.questions = questions
        self.resumes = resumes

    async def prepare_video_verification(
        self, application: Application, question_id: int
    ) -> VideoVerification:
        if application.purged_at is not None:
            raise VideoFlowError(410, "Application data was removed")
        if application.status == "rejected":
            raise VideoFlowError(403, "Application was rejected")
        if application.screening_invited_at is None:
            raise VideoFlowError(403, "Screening is not available yet")

        resume = self.resumes.get_by_application(application.id)
        if resume is None or resume.status != "done":
            raise VideoFlowError(409, "Resume is not processed yet")

        question = self.questions.get_by_id(question_id)
        if (
            question is None
            or question.vacancy_id != application.vacancy_id
            or question.type != "video"
        ):
            raise VideoFlowError(404, "Video question not found")

        return self.videos.get_or_create(application.id, question_id)
