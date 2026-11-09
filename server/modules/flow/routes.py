from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from ioc.index import ApplicationsServiceDep, S3ServiceDep
from modules.applications.dto.create_application_dto import CreateApplicationDTO
from modules.flow.dependencies import ActiveApplicationDep
from starlette import status

from config import BUCKET_NAME

router = APIRouter(prefix="/flow", tags=["flow"])


@cbv(router)
class FlowRouter:
    s3Service: S3ServiceDep
    applications_service: ApplicationsServiceDep

    @router.post("/resume-get-presigned-post-url", status_code=status.HTTP_201_CREATED)
    async def get_presigned_url_and_create_application(self, dto: CreateApplicationDTO):
        application = await self.applications_service.create_application(dto)
        s3_key = self.s3Service.get_resume_key(application.id)
        presigned_url = self.s3Service.create_presigned_post_url(BUCKET_NAME, s3_key)

        return presigned_url

    @router.get("/screening/{token}")
    async def get_screening(self, application: ActiveApplicationDep):
        return {
            "application_id": application.id,
            "vacancy_id": application.vacancy_id,
            "status": application.status,
        }
