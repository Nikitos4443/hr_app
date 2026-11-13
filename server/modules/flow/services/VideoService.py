from hr_core.models.application_model import Application
from hr_core.models.video_verification_model import VideoVerification
from hr_core.repository_interfaces.IQuestionsRepository import IQuestionsRepository
from hr_core.repository_interfaces.IResumeVerificationRepository import (
    IResumeVerificationRepository,
)
from hr_core.repository_interfaces.IVideoVerificationRepository import (
    IVideoVerificationRepository,
)
from modules.flow.guards import get_answerable_question
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
        get_answerable_question(application, question_id, "video", self.questions, self.resumes)
        return self.videos.get_or_create(application.id, question_id)
