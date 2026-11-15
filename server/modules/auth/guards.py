from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request
from guard import SecurityDecorator
from jwt import PyJWTError
from pydantic import ValidationError
from starlette import status

from config import ALGORITHM, SECRET_KEY, security_config
from hr_core.models.user_model import UserRole
from modules.auth.dto.principal import AuthPrincipal

guard_deco = SecurityDecorator(security_config)


def _decode_principal(token: str) -> AuthPrincipal | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return AuthPrincipal(
            id=payload["id"],
            username=payload["sub"],
            role=payload["role"],
        )
    except PyJWTError, KeyError, ValidationError:
        return None


def verify_jwt(request, credential: str) -> AuthPrincipal | None:
    return _decode_principal(credential)


def require_auth():
    return guard_deco.require_auth(type="bearer", verifier=verify_jwt)


def require_roles(*roles: UserRole):
    allowed = frozenset(UserRole(role) for role in roles)

    def verify_role(request, credential: str) -> AuthPrincipal | None:
        principal = _decode_principal(credential)
        if principal is None or principal.role not in allowed:
            return None
        return principal

    return guard_deco.require_auth(type="bearer", verifier=verify_role)


def get_current_principal(request: Request) -> AuthPrincipal:
    principal = getattr(request.state, "auth_principal", None)
    if principal is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return principal


CurrentPrincipalDep = Annotated[AuthPrincipal, Depends(get_current_principal)]
