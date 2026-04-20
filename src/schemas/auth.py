from pydantic import BaseModel, EmailStr, SecretStr
from enum import StrEnum


class Role(StrEnum):
    LIBRARIAN = "librarian"
    PATRON = "patron"
    AUTHOR = "author"


class User(BaseModel):
    username: str
    password: SecretStr


class UserRegister(User):
    email: EmailStr
    role: Role


class UserRegisterResponse(BaseModel):
    username: str
    email: EmailStr
    role: Role


class TokenData(BaseModel):
    access_token: str
    token_type: str
