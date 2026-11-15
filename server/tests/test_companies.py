from starlette import status

from hr_core.sql.tables.users import Users


def register_admin(client, username):
    body = {"username": username, "password": "secret123", "confirm_password": "secret123"}
    assert client.post("/auth/", json=body).status_code == status.HTTP_201_CREATED
    return login(client, username)


def login(client, username):
    response = client.post("/auth/token", data={"username": username, "password": "secret123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def create_company(client, admin, name="Acme"):
    return client.post("/companies/", headers=admin, json={"name": name})


def test_admin_creates_company_and_is_attached(client):
    admin = register_admin(client, "boss")

    response = create_company(client, admin, name="  Acme ")

    assert response.status_code == status.HTTP_201_CREATED
    company = response.json()
    assert company["name"] == "Acme"
    # The admin can now manage users, which requires being attached to a company.
    assert client.get("/users/", headers=admin).status_code == status.HTTP_200_OK
    assert client.get(f"/companies/{company['id']}", headers=admin).status_code == 200


def test_admin_cannot_create_second_company(client):
    admin = register_admin(client, "boss")
    create_company(client, admin)

    assert create_company(client, admin, name="Other").status_code == status.HTTP_409_CONFLICT


def test_company_name_must_be_unique(client):
    create_company(client, register_admin(client, "boss"))

    response = create_company(client, register_admin(client, "boss2"))

    assert response.status_code == status.HTTP_409_CONFLICT


def test_empty_name_is_rejected(client):
    admin = register_admin(client, "boss")

    response = client.post("/companies/", headers=admin, json={"name": "  "})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_company(client):
    admin = register_admin(client, "boss")
    company_id = create_company(client, admin).json()["id"]

    response = client.patch(
        f"/companies/{company_id}",
        headers=admin,
        json={"name": "Acme Inc", "website": "https://acme.test"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Acme Inc"
    assert response.json()["website"] == "https://acme.test"


def test_admin_cannot_access_other_company(client):
    admin = register_admin(client, "boss")
    other = register_admin(client, "boss2")
    create_company(client, admin, name="Mine")
    other_id = create_company(client, other, name="Theirs").json()["id"]

    assert client.get(f"/companies/{other_id}", headers=admin).status_code == 404
    patch = client.patch(f"/companies/{other_id}", headers=admin, json={"name": "x"})
    assert patch.status_code == 404
    assert client.delete(f"/companies/{other_id}", headers=admin).status_code == 404


def test_hr_cannot_use_companies(client):
    admin = register_admin(client, "boss")
    company_id = create_company(client, admin).json()["id"]
    client.post("/users/", headers=admin, json={"username": "anna", "password": "secret123"})
    hr = login(client, "anna")

    assert client.get(f"/companies/{company_id}", headers=hr).status_code == 401
    assert create_company(client, hr, name="X").status_code == 401
    assert client.delete(f"/companies/{company_id}", headers=hr).status_code == 401


def test_companies_require_authentication(client):
    assert client.get("/companies/1").status_code == status.HTTP_401_UNAUTHORIZED


def test_cannot_delete_company_with_other_users(client):
    admin = register_admin(client, "boss")
    company_id = create_company(client, admin).json()["id"]
    client.post("/users/", headers=admin, json={"username": "anna", "password": "secret123"})

    response = client.delete(f"/companies/{company_id}", headers=admin)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert client.get(f"/companies/{company_id}", headers=admin).status_code == 200


def test_delete_company_when_only_admin_left(client, session_factory):
    admin = register_admin(client, "boss")
    company_id = create_company(client, admin).json()["id"]

    assert client.delete(f"/companies/{company_id}", headers=admin).status_code == 204

    assert client.get(f"/companies/{company_id}", headers=admin).status_code == 404
    with session_factory() as db:
        assert db.query(Users).filter_by(username="boss").one().company_id is None
    # The admin can create a new company afterwards.
    assert create_company(client, admin, name="Again").status_code == status.HTTP_201_CREATED


def test_delete_company_after_removing_its_users(client):
    admin = register_admin(client, "boss")
    company_id = create_company(client, admin).json()["id"]
    created = client.post(
        "/users/", headers=admin, json={"username": "anna", "password": "secret123"}
    ).json()
    client.delete(f"/users/{created['id']}", headers=admin)

    assert client.delete(f"/companies/{company_id}", headers=admin).status_code == 204
