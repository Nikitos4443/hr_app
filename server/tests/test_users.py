import jwt
from starlette import status

from hr_core.sql.tables.users import Users


def login(client, username, password="secret123"):
    response = client.post("/auth/token", data={"username": username, "password": password})
    assert response.status_code == status.HTTP_200_OK
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def register_admin(client, session_factory, username, company_id=1, password="secret123"):
    """Register an admin and attach them to a company (company creation is a separate flow)."""
    response = client.post(
        "/auth/",
        json={"username": username, "password": password, "confirm_password": password},
    )
    assert response.status_code == status.HTTP_201_CREATED
    with session_factory() as db:
        db.query(Users).filter_by(username=username).update({"company_id": company_id})
        db.commit()
    return login(client, username, password)


def register_hr(client, admin, username):
    response = client.post(
        "/users/", headers=admin, json={"username": username, "password": "secret123"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    return login(client, username)


def user_id(client, headers, username):
    users = client.get("/users/", headers=headers).json()
    return next(u["id"] for u in users if u["username"] == username)


def test_admin_creates_hr_in_own_company(client, session_factory):
    admin = register_admin(client, session_factory, "boss")

    response = client.post(
        "/users/", headers=admin, json={"username": "Anna", "password": "secret123"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["username"] == "anna"
    assert body["role"] == "hr"
    assert body["company_id"] == 1
    assert "password" not in body
    assert login(client, "anna")


def test_admin_without_company_cannot_manage_users(client):
    client.post(
        "/auth/",
        json={"username": "boss", "password": "secret123", "confirm_password": "secret123"},
    )
    admin = login(client, "boss")

    assert client.get("/users/", headers=admin).status_code == status.HTTP_403_FORBIDDEN
    create = client.post("/users/", headers=admin, json={"username": "abc", "password": "x"})
    assert create.status_code == status.HTTP_403_FORBIDDEN


def test_duplicate_username_is_conflict(client, session_factory):
    admin = register_admin(client, session_factory, "boss")

    response = client.post("/users/", headers=admin, json={"username": "boss", "password": "x"})

    assert response.status_code == status.HTTP_409_CONFLICT


def test_registration_duplicate_username_is_conflict(client):
    body = {"username": "john", "password": "a", "confirm_password": "a"}
    client.post("/auth/", json=body)

    assert client.post("/auth/", json=body).status_code == status.HTTP_409_CONFLICT


def test_admin_lists_only_own_company(client, session_factory):
    admin = register_admin(client, session_factory, "boss", company_id=1)
    register_hr(client, admin, "mine")
    other_admin = register_admin(client, session_factory, "boss2", company_id=2)
    register_hr(client, other_admin, "other")

    names = {u["username"] for u in client.get("/users/", headers=admin).json()}

    assert names == {"boss", "mine"}


def test_admin_cannot_touch_other_company(client, session_factory):
    admin = register_admin(client, session_factory, "boss", company_id=1)
    other_admin = register_admin(client, session_factory, "boss2", company_id=2)
    register_hr(client, other_admin, "other")
    other_id = user_id(client, other_admin, "other")

    assert client.get(f"/users/{other_id}", headers=admin).status_code == 404
    patch = client.patch(f"/users/{other_id}", headers=admin, json={"username": "xxx"})
    assert patch.status_code == 404
    assert client.delete(f"/users/{other_id}", headers=admin).status_code == 404
    assert client.get(f"/users/{other_id}", headers=other_admin).status_code == 200


def test_admin_updates_and_deletes_company_user(client, session_factory):
    admin = register_admin(client, session_factory, "boss")
    register_hr(client, admin, "mine")
    uid = user_id(client, admin, "mine")

    updated = client.patch(
        f"/users/{uid}", headers=admin, json={"username": "renamed", "role": "company_admin"}
    )
    assert updated.status_code == 200
    assert updated.json()["username"] == "renamed"
    assert updated.json()["role"] == "company_admin"

    assert client.delete(f"/users/{uid}", headers=admin).status_code == 204
    assert client.get(f"/users/{uid}", headers=admin).status_code == 404


def test_hr_gets_and_updates_only_self(client, session_factory):
    admin = register_admin(client, session_factory, "boss")
    hr = register_hr(client, admin, "anna")
    me = user_id(client, admin, "anna")
    other = user_id(client, admin, "boss")

    assert client.get(f"/users/{me}", headers=hr).json()["username"] == "anna"
    assert client.get(f"/users/{other}", headers=hr).status_code == 403
    assert client.patch(f"/users/{other}", headers=hr, json={"username": "hack"}).status_code == 403

    response = client.patch(f"/users/{me}", headers=hr, json={"password": "newsecret1"})
    assert response.status_code == 200
    assert login(client, "anna", "newsecret1")


def test_hr_cannot_change_own_role(client, session_factory):
    admin = register_admin(client, session_factory, "boss")
    hr = register_hr(client, admin, "anna")
    me = user_id(client, admin, "anna")

    response = client.patch(f"/users/{me}", headers=hr, json={"role": "company_admin"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_hr_cannot_use_admin_endpoints(client, session_factory):
    admin = register_admin(client, session_factory, "boss")
    hr = register_hr(client, admin, "anna")

    assert client.get("/users/", headers=hr).status_code == 401
    create = client.post("/users/", headers=hr, json={"username": "abc", "password": "x"})
    assert create.status_code == 401
    assert client.delete("/users/1", headers=hr).status_code == 401


def test_users_require_authentication(client):
    assert client.get("/users/").status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_without_company_can_read_own_profile(client):
    response = client.post(
        "/auth/",
        json={"username": "lonely", "password": "secret123", "confirm_password": "secret123"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    token = response.json()["access_token"]
    uid = jwt.decode(token, options={"verify_signature": False})["id"]

    response = client.get(f"/users/{uid}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["company_id"] is None
