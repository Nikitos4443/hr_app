from hr_core.models.application_model import Application
from hr_core.repository_interfaces.IApplicationsRepository import IApplicationsRepository
from modules.applications.IApplicationService import IApplicationService
from modules.applications.dto.create_application_dto import CreateApplicationDTO


class ApplicationsService(IApplicationService):
    def __init__(self, repo: IApplicationsRepository):
        self.repo = repo

    async def create_application(self, dto: CreateApplicationDTO):
        application_model = Application(
            email=dto.email,
            vacancy_id=dto.vacancy_id,
            status="pending",
        )

        return self.repo.create(application_model)

    async def get_by_screening_token(self, token: str) -> Application | None:
        return self.repo.get_by_screening_token(token)
