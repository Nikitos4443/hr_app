from sqlalchemy.orm import Session
from ..IDatabaseProvider import IDatabaseProvider
from ...models import User
from .database import Base, engine, session_local
from .user_model import UserTable

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


def get_sql_provider():
    db = session_local()
    try:
        yield SQLDatabaseProvider(db)
    finally:
        db.close()
