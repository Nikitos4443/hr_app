import os

# Set before importing the app: auth.auth reads SECRET_KEY at import time,
# and CI has no .env file.
os.environ["SECRET_KEY"] = "test-secret-key-at-least-32-bytes-long"
os.environ["ALGORITHM"] = "HS256"
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from auth.database_providers import get_provider
from auth.database_providers.sql.database import Base
from auth.database_providers.sql.SQLDatabaseProvider import SQLDatabaseProvider


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    def override_get_provider():
        db = testing_session()
        try:
            yield SQLDatabaseProvider(db)
        finally:
            db.close()

    app.dependency_overrides[get_provider] = override_get_provider
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    engine.dispose()
