from dataclasses import dataclass


@dataclass
class User:
    username: str
    email: str
    hashed_password: str
    role: str
