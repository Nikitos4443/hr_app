from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv
from starlette import status

from config import BUCKET_NAME
from hr_core.s3.service import S3Service
from ioc.index import S3ServiceDep, ResumeServiceDep, ApplicationsServiceDep, VideoServiceDep
from modules.applications.dto.create_application_dto import CreateApplicationDTO
from modules.flow.dependencies import ActiveApplicationDep
from modules.flow.dto.create_resume_verification_dto import CreateResumeVerificationDTO
from modules.flow.errors import VideoFlowError

router = APIRouter(prefix="/flow", tags=["flow"])

@cbv(router)
class FlowRouter:
    s3Service: S3ServiceDep
    applications_service: ApplicationsServiceDep
    resume_service: ResumeServiceDep
    video_service: VideoServiceDep

    @router.post("/resume-get-presigned-post-url", status_code=status.HTTP_201_CREATED)
    async def get_resume_presigned_url_and_create_application(
            self,
            dto: CreateApplicationDTO
    ):
        application = await self.applications_service.create_application(dto)
        s3_key = self.s3Service.get_resume_key(application.id)

        presigned_post = self.s3Service.create_presigned_post_url(BUCKET_NAME, s3_key)
        if presigned_post is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to create resume upload URL",
            )

        try:
            await self.resume_service.create_resume_verification(
                CreateResumeVerificationDTO(application_id=application.id, status="pending")
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create resume verification",
            )

        return presigned_post

    @router.get("/screening/{token}")
    async def get_screening(self, application: ActiveApplicationDep):
        return {
            "application_id": application.id,
            "vacancy_id": application.vacancy_id,
            "status": application.status,
        }


    @router.post(
        "/screening/{token}/questions/{question_id}/video-upload-url",
        status_code=status.HTTP_201_CREATED,
    )
    async def get_video_presigned_url(self, application: ActiveApplicationDep, question_id: int):
        try:
            verification = await self.video_service.prepare_video_verification(
                application, question_id
            )
        except VideoFlowError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        s3_key = self.s3Service.get_video_key(verification.id)
        presigned_post = self.s3Service.create_video_presigned_post_url(BUCKET_NAME, s3_key)
        if presigned_post is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to create video upload URL",
            )
        return presigned_post
