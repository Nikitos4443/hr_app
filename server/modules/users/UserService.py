import bcrypt
from fastapi import HTTPException
from starlette import status

from hr_core.models.user_model import User, UserRole
from hr_core.repository_interfaces.IUsersRepository import (
    IUsersRepository,
    UserHasDependenciesError,
)
from modules.auth.dto.principal import AuthPrincipal
from modules.users.dto.create_user_dto import CreateCompanyUserDTO, CreateUserDTO
from modules.users.dto.update_user_dto import UpdateUserDTO
from modules.users.IUserService import IUserService


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


class UserService(IUserService):
    def __init__(self, repo: IUsersRepository):
        self.repo = repo

    def create_user(self, dto: CreateUserDTO) -> User:
        if self.get_by_username(dto.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username is already taken"
            )
        return self.repo.create_user(
            User(
                username=dto.username,
                password=_hash_password(dto.password),
                role=dto.role,
                company_id=dto.company_id,
            )
        )

    def get_by_id(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)

    def list_company_members(self, company_id: int) -> list[User]:
        return self.repo.list_by_company(company_id)

    def set_company(self, user_id: int, company_id: int | None) -> User:
        user = self.repo.get_by_id(user_id)
        user.company_id = company_id
        return self.repo.update_user(user)

    def get_by_username(self, username: str) -> User | None:
        return self.repo.query_user(username)

    def create_company_user(self, actor: AuthPrincipal, dto: CreateCompanyUserDTO) -> User:
        admin = self._require_admin(actor)
        return self.create_user(
            CreateUserDTO(
                username=dto.username,
                password=dto.password,
                role=dto.role,
                company_id=admin.company_id,
            )
        )

    def list_users(self, actor: AuthPrincipal) -> list[User]:
        admin = self._require_admin(actor)
        return self.repo.list_by_company(admin.company_id)

    def get_user(self, actor: AuthPrincipal, user_id: int) -> User:
        return self._get_accessible(actor, user_id)[1]

    def update_user(self, actor: AuthPrincipal, user_id: int, dto: UpdateUserDTO) -> User:
        current, target = self._get_accessible(actor, user_id)
        if dto.role is not None and current.role != UserRole.COMPANY_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Only an admin can change roles"
            )
        if dto.username is not None and dto.username != target.username:
            if self.repo.query_user(dto.username):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Username is already taken"
                )
            target.username = dto.username
        if dto.password is not None:
            target.password = _hash_password(dto.password)
        if dto.role is not None:
            target.role = dto.role
        return self.repo.update_user(target)

    def delete_user(self, actor: AuthPrincipal, user_id: int) -> None:
        _, target = self._get_accessible(actor, user_id, admin_only=True)
        try:
            self.repo.delete_user(target.id)
        except UserHasDependenciesError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User still owns vacancies and cannot be deleted",
            ) from e

    def _load_actor(self, actor: AuthPrincipal) -> User:
        current = self.repo.get_by_id(actor.id)
        if current is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return current

    def _require_admin(self, actor: AuthPrincipal) -> User:
        current = self._load_actor(actor)
        if current.role != UserRole.COMPANY_ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
        if current.company_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Admin is not attached to a company"
            )
        return current

    def _get_accessible(
        self, actor: AuthPrincipal, user_id: int, admin_only: bool = False
    ) -> tuple[User, User]:
        current = self._require_admin(actor) if admin_only else self._load_actor(actor)
        # Self-access must work even before an admin has created a company.
        if not admin_only and current.id == user_id:
            return current, current
        if current.role == UserRole.COMPANY_ADMIN:
            target = self.repo.get_by_id(user_id) if current.company_id is not None else None
            if target is None or target.company_id != current.company_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return current, target
        if current.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return current, current
