from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from src.core.exceptions.auth import DuplicateUser, InvalidCredentials
from src.entities.user import User
from src.repositories.base import Repository
from src.schemas.auth import UserRegister


@dataclass
class AuthManager:
    user_repo: Repository[User]
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str
    password_hasher = PasswordHash.recommended()

    def _create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes
        )
        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def register_user(self, user: UserRegister) -> User:
        if await self.user_repo.get_by_id(entity_id=user.username):
            raise DuplicateUser(username=user.username)
        plain_passwd: str = user.password.get_secret_value()
        hashed_passwd: str = self.password_hasher.hash(plain_passwd)
        user_dict = user.model_dump()
        user_dict.pop("password")
        user = User(**user_dict, hashed_password=hashed_passwd)
        await self.user_repo.save(user)
        return user

    async def login_user(self, username: str, password: str) -> str:
        user: User = await self.user_repo.get_by_id(entity_id=username)
        if not user:
            raise InvalidCredentials()
        if not self.password_hasher.verify(password, user.hashed_password):
            raise InvalidCredentials()
        return self._create_access_token(data={"sub": username, "role": user.role})
