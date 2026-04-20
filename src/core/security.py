from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, PyJWTError

from src.core.config import Settings, get_settings
from src.core.exceptions.auth import InsufficientPermissions, InvalidToken, TokenExpired
from src.schemas.auth import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


def get_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict:
    try:
        payload = jwt.decode(
            token, settings.auth.secret_key, algorithms=[settings.auth.algorithm]
        )
        username: str = payload.get("sub")
        if not username:
            raise InvalidToken("Token payload missing 'sub' field")
    except ExpiredSignatureError:
        raise TokenExpired()
    except PyJWTError:
        raise InvalidToken("General token decoding error")
    return payload


class RoleVerifier:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    def __call__(
        self, token_payload: Annotated[str, Depends(get_token_payload)]
    ) -> None:
        current_role = token_payload.get("role")
        if current_role not in self.allowed_roles:
            raise InsufficientPermissions()
