from core.exceptions.base import LibraryError


class BorrowError(LibraryError):
    pass


class BorrowNotFound(BorrowError):
    pass
