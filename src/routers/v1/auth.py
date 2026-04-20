from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.security import RoleVerifier
from src.routers.dependencies.auth import get_auth_manager
from src.schemas.auth import Role, TokenData, UserRegister, UserRegisterResponse
from src.services.auth import AuthManager

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleVerifier(allowed_roles=[Role.LIBRARIAN]))],
)
async def register(
    user: UserRegister, auth_manager: Annotated[AuthManager, Depends(get_auth_manager)]
) -> UserRegister:
    return await auth_manager.register_user(user=user)


@router.post("/token", response_model=TokenData, include_in_schema=False)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_manager: Annotated[AuthManager, Depends(get_auth_manager)],
) -> TokenData:
    token: str = await auth_manager.login_user(
        username=form_data.username, password=form_data.password
    )
    return TokenData(access_token=token, token_type="bearer")
