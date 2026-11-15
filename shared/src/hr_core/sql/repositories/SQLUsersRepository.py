from sqlalchemy import select
from sqlalchemy.orm import Session

from hr_core.models.user_model import User, UserRole
from hr_core.repository_interfaces.IUsersRepository import IUsersRepository
from hr_core.sql.tables.users import Users


class SQLUsersRepository(IUsersRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create_user(self, entity: User):
        user = Users(
            username=entity.username,
            password=entity.password,
            role=UserRole(entity.role).value,
            company_id=entity.company_id,
        )
        self.db.add(user)
        self.db.commit()

    def query_user(self, username):
        stmt = select(Users).where(Users.username == username)
        userEntity = self.db.scalars(stmt).first()
        if not userEntity:
            return
        user = User(
            id=userEntity.id,
            username=userEntity.username,
            password=userEntity.password,
            role=UserRole(userEntity.role),
            company_id=userEntity.company_id,
        )
        return user
