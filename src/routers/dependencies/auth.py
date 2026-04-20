from typing import Annotated

from fastapi.params import Depends

from src.core.config import Settings, get_settings
from src.entities.user import User
from src.repositories.base import Repository
from src.repositories.mongodb import UserMongoRepo
from src.services.auth import AuthManager


def get_user_repository() -> Repository[User]:
    return UserMongoRepo()


def get_auth_manager(
    user_repo: Annotated[Repository[User], Depends(get_user_repository)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthManager:
    return AuthManager(
        user_repo=user_repo,
        secret_key=settings.auth.secret_key,
        access_token_expire_minutes=settings.auth.access_token_expire_minutes,
        algorithm=settings.auth.algorithm,
    )
