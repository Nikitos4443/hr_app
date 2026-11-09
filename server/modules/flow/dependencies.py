from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from hr_core.models.application_model import Application
from ioc.index import ApplicationsServiceDep


async def get_active_application(token: str, service: ApplicationsServiceDep) -> Application:
    application = await service.get_by_screening_token(token)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    if application.status == "rejected":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Application was rejected")
    return application


ActiveApplicationDep = Annotated[Application, Depends(get_active_application)]
