from abc import ABC, abstractmethod

from hr_core.models.video_verification_model import VideoVerification


class IVideoVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: VideoVerification) -> VideoVerification: ...

    @abstractmethod
    def save_transcription(
        self, verification_id: int, transcription: str
    ) -> VideoVerification | None: ...
