from sqlalchemy.orm import Session
from ..IDatabaseProvider import IDatabaseProvider
from ...models import User
from .database import Base, engine, session_local
from .user_model import UserTable
from sqlalchemy import select

Base.metadata.create_all(bind=engine)


class SQLDatabaseProvider(IDatabaseProvider):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def create_user(self, entity: User):
        user = UserTable(
            username=entity.username,
            password=entity.password,
            role=entity.role
        )
        self.db.add(user)
        self.db.commit()

    def query_user(self, username):
        stmt = select(UserTable).where(UserTable.username == username)
        userEntity = self.db.scalars(stmt).first()
        if not userEntity:
            return
        user = User(id=userEntity.id, username=userEntity.username, password=userEntity.password, role=userEntity.role)
        return user


def get_sql_provider():
    db = session_local()
    try:
        yield SQLDatabaseProvider(db)
    finally:
        db.close()
