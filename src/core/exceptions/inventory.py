from core.exceptions.base import LibraryError


class InventoryError(LibraryError):
    pass


class BookNotFound(InventoryError):
    pass