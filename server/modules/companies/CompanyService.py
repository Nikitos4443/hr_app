from fastapi import HTTPException
from starlette import status

from hr_core.models.company_model import Company
from hr_core.models.user_model import User
from hr_core.repository_interfaces.ICompaniesRepository import (
    CompanyHasDependenciesError,
    ICompaniesRepository,
)
from modules.auth.dto.principal import AuthPrincipal
from modules.companies.dto.company_dto import CreateCompanyDTO, UpdateCompanyDTO
from modules.companies.ICompanyService import ICompanyService
from modules.users.IUserService import IUserService


class CompanyService(ICompanyService):
    def __init__(self, repo: ICompaniesRepository, users_service: IUserService):
        self.repo = repo
        self.users_service = users_service

    def create_company(self, actor: AuthPrincipal, dto: CreateCompanyDTO) -> Company:
        admin = self._load_actor(actor)
        if admin.company_id is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Admin already has a company"
            )
        self._ensure_name_free(dto.name)
        company = self.repo.create(
            Company(name=dto.name, description=dto.description, website=dto.website)
        )
        self.users_service.set_company(admin.id, company.id)
        return company

    def get_company(self, actor: AuthPrincipal, company_id: int) -> Company:
        return self._get_own_company(actor, company_id)[1]

    def update_company(
        self, actor: AuthPrincipal, company_id: int, dto: UpdateCompanyDTO
    ) -> Company:
        _, company = self._get_own_company(actor, company_id)
        if dto.name is not None and dto.name != company.name:
            self._ensure_name_free(dto.name)
            company.name = dto.name
        if dto.description is not None:
            company.description = dto.description
        if dto.website is not None:
            company.website = dto.website
        return self.repo.update(company)

    def delete_company(self, actor: AuthPrincipal, company_id: int) -> None:
        admin, company = self._get_own_company(actor, company_id)
        others = [
            m for m in self.users_service.list_company_members(company.id) if m.id != admin.id
        ]
        if others:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company still has users other than its admin",
            )
        try:
            self.repo.delete(company.id)
        except CompanyHasDependenciesError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company still has vacancies and cannot be deleted",
            ) from e

    def _load_actor(self, actor: AuthPrincipal) -> User:
        user = self.users_service.get_by_id(actor.id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user

    def _get_own_company(self, actor: AuthPrincipal, company_id: int) -> tuple[User, Company]:
        admin = self._load_actor(actor)
        company = self.repo.get_by_id(company_id) if admin.company_id == company_id else None
        if company is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return admin, company

    def _ensure_name_free(self, name: str) -> None:
        if self.repo.get_by_name(name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Company name is already taken"
            )
