import pytest
from modules.ai_assistant.rag import KnowledgeDocument, get_knowledge_index
from starlette import status

from app import fastapi_app as app


class FakeIndex:
    """In-memory stand-in for the pgvector index: {(company_id, source): text}."""

    def __init__(self):
        self.docs: dict[tuple[int, str], str] = {}
        self.fail = False

    async def add_document(self, company_id, source, text):
        if self.fail:
            raise ConnectionError("embeddings API is down")
        self.docs[(company_id, source)] = text
        return KnowledgeDocument(source=source, chunks=1)

    async def list_documents(self, company_id):
        return [
            KnowledgeDocument(source=source, chunks=1)
            for (cid, source) in sorted(self.docs)
            if cid == company_id
        ]

    async def delete_document(self, company_id, source):
        return 1 if self.docs.pop((company_id, source), None) is not None else 0


@pytest.fixture
def index(client):
    fake = FakeIndex()
    app.dependency_overrides[get_knowledge_index] = lambda: fake
    return fake


def login(client, username):
    response = client.post("/auth/token", data={"username": username, "password": "secret123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def admin_with_company(client, username="boss", company="Acme"):
    body = {"username": username, "password": "secret123", "confirm_password": "secret123"}
    assert client.post("/auth/", json=body).status_code == status.HTTP_201_CREATED
    headers = login(client, username)
    response = client.post("/companies/", headers=headers, json={"name": company})
    assert response.status_code == status.HTTP_201_CREATED
    return headers, response.json()["id"]


def upload(client, headers, company_id, name="benefits.md", content=b"24 vacation days"):
    return client.post(
        f"/companies/{company_id}/knowledge/",
        headers=headers,
        files={"file": (name, content, "text/markdown")},
    )


def test_upload_list_and_delete(client, index):
    admin, company_id = admin_with_company(client)

    response = upload(client, admin, company_id)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"source": "benefits.md", "chunks": 1}
    assert index.docs[(company_id, "benefits.md")] == "24 vacation days"

    listed = client.get(f"/companies/{company_id}/knowledge/", headers=admin)
    assert listed.json() == [{"source": "benefits.md", "chunks": 1}]

    deleted = client.delete(f"/companies/{company_id}/knowledge/benefits.md", headers=admin)
    assert deleted.status_code == status.HTTP_204_NO_CONTENT
    assert index.docs == {}


def test_hr_of_the_company_can_upload(client, index):
    admin, company_id = admin_with_company(client)
    response = client.post(
        "/users/", headers=admin, json={"username": "anna", "password": "secret123"}
    )
    assert response.status_code == status.HTTP_201_CREATED

    assert upload(client, login(client, "anna"), company_id).status_code == 201


def test_reupload_replaces_document(client, index):
    admin, company_id = admin_with_company(client)

    upload(client, admin, company_id, content=b"old")
    upload(client, admin, company_id, content=b"new")

    assert index.docs == {(company_id, "benefits.md"): "new"}


def test_cannot_touch_other_company(client, index):
    admin, _ = admin_with_company(client)
    _, other_id = admin_with_company(client, username="boss2", company="Other")

    assert upload(client, admin, other_id).status_code == status.HTTP_404_NOT_FOUND
    listed = client.get(f"/companies/{other_id}/knowledge/", headers=admin)
    assert listed.status_code == status.HTTP_404_NOT_FOUND
    deleted = client.delete(f"/companies/{other_id}/knowledge/x.md", headers=admin)
    assert deleted.status_code == status.HTTP_404_NOT_FOUND
    assert index.docs == {}


def test_requires_auth(client, index):
    response = client.get("/companies/1/knowledge/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_path_in_file_name_is_stripped(client, index):
    admin, company_id = admin_with_company(client)

    response = upload(client, admin, company_id, name="C:\\docs\\faq.md")

    assert response.json()["source"] == "faq.md"


@pytest.mark.parametrize(
    "name, content, code",
    [
        ("faq.pdf", b"text", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE),
        ("faq.md", b"   \n", status.HTTP_422_UNPROCESSABLE_CONTENT),
        ("faq.md", b"\xff\xfe\x00bad", status.HTTP_422_UNPROCESSABLE_CONTENT),
        ("faq.md", b"a" * (1024 * 1024 + 1), status.HTTP_413_CONTENT_TOO_LARGE),
    ],
)
def test_invalid_files_are_rejected(client, index, name, content, code):
    admin, company_id = admin_with_company(client)

    assert upload(client, admin, company_id, name=name, content=content).status_code == code
    assert index.docs == {}


def test_delete_missing_document_is_404(client, index):
    admin, company_id = admin_with_company(client)

    response = client.delete(f"/companies/{company_id}/knowledge/nope.md", headers=admin)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_indexing_failure_is_502(client, index):
    admin, company_id = admin_with_company(client)
    index.fail = True

    assert upload(client, admin, company_id).status_code == status.HTTP_502_BAD_GATEWAY


def test_without_vector_db_is_503(client):
    # No override: tests run on SQLite, so get_knowledge_index() returns None.
    admin, company_id = admin_with_company(client)

    assert upload(client, admin, company_id).status_code == status.HTTP_503_SERVICE_UNAVAILABLE
