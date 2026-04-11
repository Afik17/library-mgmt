from core.exceptions.base import LibraryError


class PatronError(LibraryError):
    pass

class PatronNotFound(PatronError):
    pass