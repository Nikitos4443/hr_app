import os

# Set before importing the app: config reads env at import time, and CI has no .env file.
os.environ["SECRET_KEY"] = "test-secret-key-at-least-32-bytes-long"
os.environ["BUCKET_NAME"] = "test-bucket"
os.environ["ALGORITHM"] = "HS256"
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite://"
os.environ["DATABASE_PROVIDER"] = "sql"
# config.settings falls back to AWS SSM for anything missing, which CI can't reach.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["GOOGLE_API_KEY"] = "test-google-api-key"
os.environ["SMTP_USER"] = "test@example.com"
os.environ["SMTP_PASSWORD"] = "test-smtp-password"
os.environ["FRONTEND_URL"] = "http://localhost:3000"
os.environ["LLM_MODEL"] = "google_genai:gemini-2.5-flash"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

from app import fastapi_app as app
from database.init_db import get_sql_db
from hr_core.sql.session import create_all_tables, create_session_factory


@pytest.fixture
def client():
    testing_session = create_session_factory(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    create_all_tables(testing_session)

    def override_get_sql_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_sql_db] = override_get_sql_db
    with TestClient(app, client=("127.0.0.1", 50000)) as test_client:
        yield test_client
    app.dependency_overrides.clear()
