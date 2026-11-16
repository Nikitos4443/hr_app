"""Companies and vacancies saved through the API are mirrored into the assistant's vector index."""

import asyncio

import pytest
from modules.ai_assistant.rag import get_knowledge_index
from modules.knowledge.sync import CatalogSync
from starlette import status

from app import fastapi_app as app
from hr_core.models.company_model import Company


class RecordingIndex:
    def __init__(self, fail: bool = False):
        self.fail = fail
        self.companies: dict[int, Company] = {}
        self.vacancies: dict[int, dict] = {}
        self.deleted: list[tuple[str, int]] = []

    async def index_company(self, company):
        if self.fail:
            raise ConnectionError("embeddings API is down")
        self.companies[company.id] = company

    async def delete_company(self, company_id):
        self.companies.pop(company_id, None)
        self.deleted.append(("company", company_id))

    async def index_vacancy(self, vacancy):
        if self.fail:
            raise ConnectionError("embeddings API is down")
        self.vacancies[vacancy.id] = vacancy.model_dump()

    async def delete_vacancy(self, vacancy_id):
        self.vacancies.pop(vacancy_id, None)
        self.deleted.append(("vacancy", vacancy_id))


@pytest.fixture
def index(client):
    recording = RecordingIndex()
    app.dependency_overrides[get_knowledge_index] = lambda: recording
    return recording


def login(client, username):
    response = client.post("/auth/token", data={"username": username, "password": "secret123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def admin_with_company(client, name="Acme"):
    body = {"username": "boss", "password": "secret123", "confirm_password": "secret123"}
    client.post("/auth/", json=body)
    admin = login(client, "boss")
    response = client.post("/companies/", headers=admin, json={"name": name})
    assert response.status_code == status.HTTP_201_CREATED
    return admin, response.json()["id"]


def test_company_create_update_delete_is_synced(client, index):
    admin, company_id = admin_with_company(client)
    assert index.companies[company_id].name == "Acme"

    client.patch(f"/companies/{company_id}", headers=admin, json={"description": "We sell rockets"})
    assert index.companies[company_id].description == "We sell rockets"

    response = client.delete(f"/companies/{company_id}", headers=admin)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert company_id not in index.companies


def test_vacancy_create_update_delete_is_synced(client, index):
    admin, company_id = admin_with_company(client)

    vacancy = client.post(
        "/vacancies/", headers=admin, json={"title": "Python dev", "salary_min": 3000}
    ).json()
    assert index.vacancies[vacancy["id"]]["salary_min"] == 3000
    assert index.vacancies[vacancy["id"]]["company_id"] == company_id

    client.patch(f"/vacancies/{vacancy['id']}", headers=admin, json={"salary_min": 3500})
    assert index.vacancies[vacancy["id"]]["salary_min"] == 3500

    response = client.delete(f"/vacancies/{vacancy['id']}", headers=admin)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert index.deleted == [("vacancy", vacancy["id"])]


def test_failed_request_is_not_synced(client, index):
    admin, _ = admin_with_company(client)

    response = client.patch("/vacancies/999", headers=admin, json={"salary_min": 1})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert index.vacancies == {}


def test_index_failure_does_not_break_saving(client):
    app.dependency_overrides[get_knowledge_index] = lambda: RecordingIndex(fail=True)
    admin, _ = admin_with_company(client)

    response = client.post("/vacancies/", headers=admin, json={"title": "Python dev"})

    assert response.status_code == status.HTTP_201_CREATED


def test_sync_without_vector_db_is_noop():
    sync = CatalogSync(index=None)

    asyncio.run(sync.company_saved(Company(id=1, name="Acme")))
    asyncio.run(sync.vacancy_deleted(1))
