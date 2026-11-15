from datetime import timedelta

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from fastapi_utils.cbv import cbv
from guard import SecurityMiddleware
from modules.auth.AuthService import AuthService
from modules.auth.guards import CurrentPrincipalDep, guard_deco, require_auth, require_roles
from starlette import status

from config import security_config
from hr_core.models.user_model import UserRole


@pytest.fixture
def guarded_client():
    app = FastAPI()
    app.add_middleware(SecurityMiddleware, config=security_config)
    app.state.guard_decorator = guard_deco

    @app.get("/any")
    @require_auth()
    def any_user(principal: CurrentPrincipalDep):
        return principal

    @app.get("/admin")
    @require_roles(UserRole.COMPANY_ADMIN)
    def admin_only(principal: CurrentPrincipalDep):
        return principal

    @app.get("/staff")
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def staff(principal: CurrentPrincipalDep):
        return principal

    router = APIRouter(prefix="/cbv")

    @cbv(router)
    class Handler:
        @router.get("/me")
        @require_roles(UserRole.HR)
        async def me(self, principal: CurrentPrincipalDep):
            return principal

    app.include_router(router)

    with TestClient(app, client=("127.0.0.1", 50000)) as client:
        yield client


def bearer(role, user_id=1, username="john"):
    token = AuthService(repo=None).create_access_token(
        username, user_id, role, timedelta(minutes=5)
    )
    return {"Authorization": f"Bearer {token}"}


def test_missing_token_is_unauthorized(guarded_client):
    assert guarded_client.get("/any").status_code == status.HTTP_401_UNAUTHORIZED


def test_garbage_token_is_unauthorized(guarded_client):
    response = guarded_client.get("/any", headers={"Authorization": "Bearer nope"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_endpoint_receives_jwt_data(guarded_client):
    response = guarded_client.get("/any", headers=bearer("hr", user_id=7, username="anna"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 7, "username": "anna", "role": "hr"}


def test_role_restriction(guarded_client):
    assert guarded_client.get("/admin", headers=bearer("hr")).status_code == 401
    assert guarded_client.get("/admin", headers=bearer("company_admin")).status_code == 200


def test_multiple_roles_on_async_endpoint(guarded_client):
    assert guarded_client.get("/staff", headers=bearer("hr")).status_code == 200
    assert guarded_client.get("/staff", headers=bearer("company_admin")).status_code == 200


def test_token_with_unknown_role_is_rejected(guarded_client):
    assert guarded_client.get("/any", headers=bearer("superuser")).status_code == 401


def test_works_on_class_based_routes(guarded_client):
    assert guarded_client.get("/cbv/me").status_code == 401
    assert guarded_client.get("/cbv/me", headers=bearer("company_admin")).status_code == 401
    assert guarded_client.get("/cbv/me", headers=bearer("hr")).status_code == 200
