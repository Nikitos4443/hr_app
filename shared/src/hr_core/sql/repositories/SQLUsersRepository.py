from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hr_core.models.user_model import User, UserRole
from hr_core.repository_interfaces.IUsersRepository import (
    IUsersRepository,
    UserHasDependenciesError,
)
from hr_core.sql.tables.users import Users


def _to_model(row: Users) -> User:
    return User(
        id=row.id,
        username=row.username,
        password=row.password,
        role=UserRole(row.role),
        company_id=row.company_id,
        created_at=row.created_at,
    )


class SQLUsersRepository(IUsersRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create_user(self, entity: User) -> User:
        user = Users(
            username=entity.username,
            password=entity.password,
            role=UserRole(entity.role).value,
            company_id=entity.company_id,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return _to_model(user)

    def query_user(self, username: str) -> User | None:
        stmt = select(Users).where(Users.username == username)
        row = self.db.scalars(stmt).first()
        return _to_model(row) if row else None

    def get_by_id(self, user_id: int) -> User | None:
        row = self.db.get(Users, user_id)
        return _to_model(row) if row else None

    def list_by_company(self, company_id: int) -> list[User]:
        stmt = select(Users).where(Users.company_id == company_id).order_by(Users.id)
        return [_to_model(row) for row in self.db.scalars(stmt)]

    def update_user(self, entity: User) -> User:
        row = self.db.get(Users, entity.id)
        row.username = entity.username
        row.password = entity.password
        row.role = UserRole(entity.role).value
        row.company_id = entity.company_id
        self.db.commit()
        self.db.refresh(row)
        return _to_model(row)

    def delete_user(self, user_id: int) -> None:
        row = self.db.get(Users, user_id)
        if row is None:
            return
        try:
            self.db.delete(row)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise UserHasDependenciesError from e
