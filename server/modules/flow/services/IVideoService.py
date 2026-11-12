from abc import ABC, abstractmethod

from hr_core.models.application_model import Application
from hr_core.models.video_verification_model import VideoVerification


class IVideoService(ABC):
    @abstractmethod
    async def prepare_video_verification(
        self, application: Application, question_id: int
    ) -> VideoVerification: ...
