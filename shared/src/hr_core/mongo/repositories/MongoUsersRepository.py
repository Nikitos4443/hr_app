from pymongo.database import Database

from hr_core.models.user_model import User
from hr_core.repository_interfaces.IUsersRepository import IUsersRepository


class MongoUsersRepository(IUsersRepository):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db

    def create_user(self, entity: User):
        pass

    def query_user(self, username):
        pass

    def get_by_id(self, user_id):
        pass

    def list_by_company(self, company_id):
        pass

    def update_user(self, entity: User):
        pass

    def delete_user(self, user_id):
        pass
