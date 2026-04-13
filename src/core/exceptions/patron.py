from core.exceptions.base import LibraryError


class PatronError(LibraryError):
    pass


class PatronNotFound(PatronError):
    def __init__(self, patron_id: str):
        super().__init__(f"Patron {patron_id} not found", 404)

class DuplicatePatron(PatronError):
    def __init__(self, patron_id: str):
        super().__init__(f"Patron {patron_id} already exists", 409)