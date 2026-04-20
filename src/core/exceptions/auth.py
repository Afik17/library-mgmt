from fastapi import status

from src.core.exceptions.base import LibraryError


class AuthError(LibraryError):
    pass


class DuplicateUser(AuthError):
    def __init__(self, username: str):
        super().__init__(f"User {username} already exists", status.HTTP_409_CONFLICT)


class InvalidCredentials(AuthError):
    def __init__(self):
        super().__init__("Invalid username or password", status.HTTP_401_UNAUTHORIZED)


class TokenExpired(AuthError):
    def __init__(self):
        super().__init__("Token has expired", status.HTTP_401_UNAUTHORIZED)


class InvalidToken(AuthError):
    def __init__(self, msg: str):
        super().__init__(f"Invalid token, {msg}", status.HTTP_401_UNAUTHORIZED)


class InsufficientPermissions(AuthError):
    def __init__(self):
        super().__init__(
            "Insufficient permissions to access this resource",
            status.HTTP_403_FORBIDDEN,
        )
