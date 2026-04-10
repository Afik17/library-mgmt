from abc import ABC, abstractmethod
from typing import Optional

from models.patron import Patron
from models.book import Book
from models.borrow import Borrow


class BookRepo(ABC):
    @abstractmethod
    def save(self, book: Book) -> None:
        pass

    @abstractmethod
    def update(self, book: Book) -> None:
        pass

    @abstractmethod
    def remove(self, book_id: str) -> None:
        pass

    @abstractmethod
    def get_by_id(self, book_id: str) -> Optional[Book]:
        pass

    @abstractmethod
    def find_by_criteria(self, **criteria) -> list[Book]:
        pass

    @abstractmethod
    def get_all(self) -> list[Book]:
        pass


class PatronRepo(ABC):
    @abstractmethod
    def save(self, patron: Patron) -> None:
        pass

    @abstractmethod
    def update(self, patron: Patron) -> None:
        pass

    @abstractmethod
    def remove(self, patron_id: str) -> None:
        pass

    @abstractmethod
    def get_by_id(self, patron_id: str) -> Optional[Patron]:
        pass

    @abstractmethod
    def find_by_criteria(self, **criteria: any) -> list[Patron]:
        pass

    @abstractmethod
    def get_all() -> list[Patron]:
        pass


class BorrowRepo(ABC):
    @abstractmethod
    def save(borrow: Borrow) -> None:
        pass

    @abstractmethod
    def update(borrow: Borrow) -> None:
        pass

    @abstractmethod
    def remove(borrow_id: str) -> None:
        pass

    @abstractmethod
    def get_by_id(borrow_id: str) -> Optional[Borrow]:
        pass

    @abstractmethod
    def find_by_criteria(self, **criteria: any) -> list[Borrow]:
        pass

    @abstractmethod
    def get_all() -> list[Borrow]:
        pass
