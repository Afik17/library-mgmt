from core.exceptions.base import LibraryError


class BorrowError(LibraryError):
    pass


class BorrowNotFound(BorrowError):
    def __init__(self, borrow_id: str):
        super().__init__(f"Borrow {borrow_id} not found", 404)
