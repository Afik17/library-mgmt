from core.exceptions.base import LibraryError


class InventoryError(LibraryError):
    pass


class BookNotFound(InventoryError):
    def __init__(self, book_id: str):
        super().__init__(f"Book {book_id} not found", 404)