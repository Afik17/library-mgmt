from core.exceptions.base import LibraryError


class InventoryError(LibraryError):
    pass


class BookNotFound(InventoryError):
    def __init__(self, book_id: str):
        super().__init__(f"Book {book_id} not found", 404)


class DuplicateBook(InventoryError):
    def __init__(self, title: str, author: str):
        super().__init__(f"The Book {title}, by {author}, already exists", 409)


class BookUnAvailable(InventoryError):
    def __init__(self, book_id: str):
        super().__init__(f"There is not avaiable copy of Book {book_id}", 451)
