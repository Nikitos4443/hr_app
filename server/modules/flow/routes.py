from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from ioc.index import (
    get_applications_service,
    get_resume_service,
    get_s3_service,
    get_screening_service,
    get_text_service,
    get_video_service,
)
from starlette import status

from config import BUCKET_NAME
from hr_core.s3.service import S3Service
from modules.applications.dto.create_application_dto import CreateApplicationDTO
from modules.applications.IApplicationService import IApplicationService
from modules.flow.dependencies import ActiveApplicationDep
from modules.flow.dto.create_resume_verification_dto import CreateResumeVerificationDTO
from modules.flow.dto.save_text_answer_dto import SaveTextAnswerDTO
from modules.flow.dto.screening_dto import ScreeningResponse
from modules.flow.errors import ScreeningError
from modules.flow.services.IResumeService import IResumeService
from modules.flow.services.ITextService import ITextService
from modules.flow.services.IVideoService import IVideoService
from modules.flow.services.ScreeningService import ScreeningService

router = APIRouter(prefix="/flow", tags=["flow"])


@cbv(router)
class FlowRouter:
    s3Service: S3Service = Depends(get_s3_service)
    applications_service: IApplicationService = Depends(get_applications_service)
    resume_service: IResumeService = Depends(get_resume_service)
    video_service: IVideoService = Depends(get_video_service)
    text_service: ITextService = Depends(get_text_service)
    screening_service: ScreeningService = Depends(get_screening_service)

    @router.post("/resume-get-presigned-post-url", status_code=status.HTTP_201_CREATED)
    async def get_resume_presigned_url_and_create_application(self, dto: CreateApplicationDTO):
        application = await self.applications_service.create_application(dto)
        s3_key = self.s3Service.get_resume_key(application.id)

        presigned_post = self.s3Service.create_presigned_post_url(BUCKET_NAME, s3_key)
        if presigned_post is None:
            await self.applications_service.delete_application(application.id)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to create resume upload URL",
            )

        try:
            await self.resume_service.create_resume_verification(
                CreateResumeVerificationDTO(application_id=application.id, status="pending")
            )
        except Exception as e:
            # Roll back so the candidate is not locked out by the duplicate-email check.
            await self.applications_service.delete_application(application.id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create resume verification",
            ) from e

        return presigned_post

    @router.get("/screening/{token}", response_model=ScreeningResponse)
    async def get_screening(self, application: ActiveApplicationDep):
        return self.screening_service.get_view(application)

    @router.post(
        "/screening/{token}/questions/{question_id}/video-upload-url",
        status_code=status.HTTP_201_CREATED,
    )
    async def get_video_presigned_url(self, application: ActiveApplicationDep, question_id: int):
        try:
            verification = await self.video_service.prepare_video_verification(
                application, question_id
            )
        except ScreeningError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail) from e

        s3_key = self.s3Service.get_video_key(verification.id)
        presigned_post = self.s3Service.create_video_presigned_post_url(BUCKET_NAME, s3_key)
        if presigned_post is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to create video upload URL",
            )
        return presigned_post

    @router.put("/screening/{token}/questions/{question_id}/text-answer")
    async def save_text_answer(
        self, application: ActiveApplicationDep, question_id: int, dto: SaveTextAnswerDTO
    ):
        try:
            verification = await self.text_service.save_answer(application, question_id, dto.answer)
        except ScreeningError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail) from e
        return {"question_id": question_id, "status": verification.status}
