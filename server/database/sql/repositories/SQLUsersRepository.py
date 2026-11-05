from database.models.user_model import User
from database.repository_interfaces.IUsersRepository import IUsersRepository
from sqlalchemy.orm import Session
from sqlalchemy import select

from database.sql.tables.users import Users

class SQLUsersRepository(IUsersRepository):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create_user(self, entity: User):
        user = Users(username=entity.username, password=entity.password, role=entity.role)
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
            role=userEntity.role,
        )
        return user