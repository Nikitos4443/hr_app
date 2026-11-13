from abc import ABC, abstractmethod

from hr_core.models.video_verification_model import VideoVerification


class IVideoVerificationRepository(ABC):
    @abstractmethod
    def create(self, entity: VideoVerification) -> VideoVerification: ...

    @abstractmethod
    def get_or_create(self, application_id: int, question_id: int) -> VideoVerification: ...

    @abstractmethod
    def save_transcription(
        self, verification_id: int, transcription: str
    ) -> VideoVerification | None: ...

    @abstractmethod
    def list_by_application(self, application_id: int) -> list[VideoVerification]: ...

    @abstractmethod
    def delete_by_application(self, application_id: int) -> None: ...
