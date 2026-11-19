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
os.environ["ANALYZER_LAMBDA_ARN"] = "arn:aws:lambda:eu-central-1:123456789012:function:analyzer"
os.environ["ANALYZER_SCHEDULER_ROLE_ARN"] = "arn:aws:iam::123456789012:role/scheduler"

import pytest
from fastapi.testclient import TestClient
from guard_core.handlers.ratelimit_handler import RateLimitManager
from ioc.index import get_analyzer_scheduler, get_notification_channel, get_s3_service
from sqlalchemy.pool import StaticPool

from app import fastapi_app as app
from database.init_db import get_sql_db
from hr_core.s3.service import S3Service
from hr_core.sql.session import create_all_tables, create_session_factory


@pytest.fixture(autouse=True)
def reset_rate_limits():
    """The in-memory rate limiter is process-wide; start every test with an empty window."""
    yield
    if RateLimitManager._instance is not None:
        RateLimitManager._instance.request_timestamps.clear()


@pytest.fixture
def session_factory():
    testing_session = create_session_factory(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    create_all_tables(testing_session)
    return testing_session


class FakeScheduler:
    """Stands in for AnalyzerScheduler so tests never talk to AWS."""

    def __init__(self):
        self.scheduled = {}
        self.cancelled = []
        self.fail = False

    def schedule(self, vacancy_id, run_at):
        if self.fail:
            raise RuntimeError("scheduler is down")
        self.scheduled[vacancy_id] = run_at

    def cancel(self, vacancy_id):
        if self.fail:
            raise RuntimeError("scheduler is down")
        self.scheduled.pop(vacancy_id, None)
        self.cancelled.append(vacancy_id)


@pytest.fixture
def fake_scheduler():
    return FakeScheduler()


class FakeChannel:
    """Collects outgoing e-mails instead of talking to SMTP."""

    def __init__(self):
        self.sent = []
        self.fail = False

    def send(self, recipient, subject, body):
        if self.fail:
            raise RuntimeError("smtp is down")
        self.sent.append((recipient, subject, body))


class FakeS3(S3Service):
    """Real key naming, no network."""

    def __init__(self):
        self.deleted = []
        self.fail_post = False

    def create_presigned_post_url(self, bucket_name, object_name, **kwargs):
        if self.fail_post:
            return None
        return {"url": f"https://s3.test/{bucket_name}", "fields": {"key": object_name}}

    def create_video_presigned_post_url(self, bucket_name, object_name, expiration=3600):
        return {"url": f"https://s3.test/{bucket_name}", "fields": {"key": object_name}}

    def create_presigned_get_url(self, bucket_name, object_name, expiration=300):
        return f"https://s3.test/{bucket_name}/{object_name}?signed"

    def delete_objects(self, bucket_name, keys):
        self.deleted.extend(keys)


@pytest.fixture
def fake_channel():
    return FakeChannel()


@pytest.fixture
def fake_s3():
    return FakeS3()


@pytest.fixture
def client(session_factory, fake_scheduler, fake_channel, fake_s3):
    testing_session = session_factory

    def override_get_sql_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_sql_db] = override_get_sql_db
    app.dependency_overrides[get_analyzer_scheduler] = lambda: fake_scheduler
    app.dependency_overrides[get_notification_channel] = lambda: fake_channel
    app.dependency_overrides[get_s3_service] = lambda: fake_s3
    with TestClient(app, client=("127.0.0.1", 50000)) as test_client:
        yield test_client
    app.dependency_overrides.clear()
