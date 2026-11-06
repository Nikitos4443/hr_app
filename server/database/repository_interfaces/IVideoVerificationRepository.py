from abc import ABC, abstractmethod

from database.models.video_verification_model import VideoVerification


class IVideoVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: VideoVerification) -> VideoVerification: ...
