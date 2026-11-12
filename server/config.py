import os

from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./hrapp.db")
SECRET_KEY = _require_env("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))
DATABASE_PROVIDER = os.getenv("DATABASE_PROVIDER", "sql")
MONGO_URI = os.getenv("MONGO_URI", "sql")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "sql")
BUCKET_NAME = _require_env("BUCKET_NAME")
