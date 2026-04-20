from beanie import Document
from pydantic import Field


class UserDoc(Document):
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    role: str

    class Settings:
        name = "users"
