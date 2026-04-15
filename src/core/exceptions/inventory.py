from fastapi import status

from src.core.exceptions.base import LibraryError


class InventoryError(LibraryError):
    pass


class BookNotFound(InventoryError):
    def __init__(self, book_id: str):
        super().__init__(f"Book {book_id} not found", status.HTTP_404_NOT_FOUND)


class BookUnavailable(InventoryError):
    def __init__(self, book_id: str):
        super().__init__(
            f"Book {book_id} is unavailable",
            status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )


class BookNotBorrowed(InventoryError):
    def __init__(self, book_id: str):
        super().__init__(f"Book {book_id} is not borrowed", status.HTTP_409_CONFLICT)
