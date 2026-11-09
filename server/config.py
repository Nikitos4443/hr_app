import os

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./hrapp.db")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))
DATABASE_PROVIDER = os.getenv("DATABASE_PROVIDER", "sql")
MONGO_URI = os.getenv("MONGO_URI", "sql")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "sql")
BUCKET_NAME = os.getenv("BUCKET_NAME")
