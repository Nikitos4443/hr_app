import jwt
from starlette import status

from config import ALGORITHM, SECRET_KEY


def register(client, username="john", password="secret123", confirm=None):
    return client.post(
        "/auth/",
        json={
            "username": username,
            "password": password,
            "confirm_password": confirm or password,
        },
    )


def test_register_returns_valid_token(client):
    response = register(client, username="John")

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["token_type"] == "bearer"
    payload = jwt.decode(body["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "john"


def test_register_rejects_mismatched_passwords(client):
    response = register(client, password="secret123", confirm="other")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_register_rejects_short_username(client):
    response = register(client, username="jo")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_login_with_valid_credentials(client):
    register(client)

    response = client.post("/auth/token", data={"username": "john", "password": "secret123"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"]


def test_login_with_wrong_password(client):
    register(client)

    response = client.post("/auth/token", data={"username": "john", "password": "nope"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_register_defaults_to_hr_role(client):
    body = register(client).json()
    payload = jwt.decode(body["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["role"] == "hr"


def test_register_company_admin_role(client):
    response = client.post(
        "/auth/",
        json={
            "username": "boss",
            "password": "secret123",
            "confirm_password": "secret123",
            "role": "company_admin",
        },
    )
    payload = jwt.decode(response.json()["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["role"] == "company_admin"


def test_register_rejects_unknown_role(client):
    response = client.post(
        "/auth/",
        json={
            "username": "boss",
            "password": "secret123",
            "confirm_password": "secret123",
            "role": "superuser",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
