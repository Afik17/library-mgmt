from entities.book import Book
from entities.borrow import Borrow
from entities.patron import Patron
from repositories.base import BookRepo, BorrowRepo, PatronRepo


class InMemoryBookRepo(BookRepo):
    def __init__(self):
        self._table = {}

    def save(self, book: Book) -> None:
        self._table[book.book_id] = book

    def update(self, book: Book):
        self._table[book.book_id] = book

    def remove(self, book_id: str):
        self._table.pop(book_id)

    def get_by_id(self, book_id: str) -> Book:
        return self._table.get(book_id)

    def find_by_criteria(self, **criteria: any) -> list[Book]:
        results = []
        all_records = self.get_all()
        for record in all_records:
            match = True
            for attr, search_value in criteria.items():
                db_value = str(getattr(record, attr, None)).lower()
                if str(search_value).lower() not in db_value:
                    match = False
                    break
            if match:
                results.append(record)
        return results

    def get_all(self) -> list[Book]:
        return list(self._table.values())


class InMemoryPatronRepo(PatronRepo):
    def __init__(self):
        self._table = {}

    def save(self, patron: Patron):
        self._table[patron.patron_id] = patron

    def update(self, patron: Patron):
        self._table[patron.patron_id] = patron

    def remove(self, patron_id: str) -> None:
        return self._table.pop(patron_id)

    def get_by_id(self, patron_id: str) -> Patron:
        return self._table.get(patron_id)

    def find_by_criteria(self, **criteria: any) -> list[Book]:
        results = []
        all_records = self.get_all()
        for record in all_records:
            match = True
            for attr, search_value in criteria.items():
                db_value = str(getattr(record, attr, None)).lower()
                if str(search_value).lower() not in db_value:
                    match = False
                    break
            if match:
                results.append(record)
        return results

    def get_all(self) -> list[Patron]:
        return list(self._table.values())


class InMemoryBorrowRepo(BorrowRepo):
    def __init__(self):
        self._table = {}

    def save(self, borrow: Borrow) -> Borrow:
        self._table[borrow.borrow_id] = borrow
        return borrow

    def update(self, borrow: Borrow) -> None:
        self._table[borrow.borrow_id] = borrow

    def remove(self, borrow_id: str) -> None:
        self._table.pop(borrow_id)

    def get_by_id(self, borrow_id: str) -> Borrow:
        return self._table.get(borrow_id)

    def find_by_criteria(self, **criteria: any) -> list[Book]:
        results = []
        all_records = self.get_all()
        for record in all_records:
            match = True
            for attr, search_value in criteria.items():
                db_value = str(getattr(record, attr, None)).lower()
                if str(search_value).lower() not in db_value:
                    match = False
                    break
            if match:
                results.append(record)
        return results

    def get_all(self) -> list[Borrow]:
        return list(self._table.values())
