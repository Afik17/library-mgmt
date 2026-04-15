from dataclasses import dataclass
from typing import Optional

from src.schemas.borrow import BorrowStatus
from src.core.exceptions.patron import PatronNotFound
from src.entities.book import Book
from src.entities.borrow import Borrow
from src.entities.patron import Patron
from src.schemas.book import (
    BookBorrow,
    BookCreate,
    BookSearchCriteria,
    BookUpdate,
)
from src.schemas.patron import PatronCreate, PatronSearchCriteria, PatronUpdate
from src.services.inventory import InventoryManager
from src.services.patron import PatronManager


@dataclass
class Library:
    inventory: InventoryManager
    patrons: PatronManager

    """ Book functions"""

    def add_book(self, book: BookCreate) -> Book:
        return self.inventory.add_book(book=book)

    def update_book(self, book_id: str, book: BookUpdate) -> Book:
        return self.inventory.update_book(book_id=book_id, book=book)

    def remove_book(self, book_id: str) -> None:
        return self.inventory.remove_book(book_id=book_id)

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        return self.inventory.book_repo.get_by_id(book_id=book_id)

    def search_books(self, criteria: BookSearchCriteria) -> list[Book]:
        return self.inventory.search_books(criteria=criteria)

    def borrow_book(self, book_id: str, book_borrow: BookBorrow) -> Borrow:
        if not self.patrons.get_patron_by_id(patron_id=book_borrow.patron_id):
            raise PatronNotFound(patron_id=book_borrow.patron_id)
        return self.inventory.borrow_book(book_id=book_id, book_borrow=book_borrow)

    def extend_borrow_book(self, book_id: str, days: int) -> Borrow:
        return self.inventory.extend_borrow_book(book_id=book_id, days=days)

    def return_book(self, book_id: str) -> Book:
        return self.inventory.return_book(book_id=book_id)

    """ Patron functions"""

    def register_new_patron(self, patron: PatronCreate) -> Patron:
        return self.patrons.register_new_patron(patron=patron)

    def update_patron(self, patron_id: str, patron: PatronUpdate) -> Patron:
        return self.patrons.update_patron(patron_id=patron_id, patron=patron)

    def remove_patron(self, patron_id: str) -> None:
        return self.patrons.remove_patron(patron_id=patron_id)

    def get_patron_by_id(self, patron_id: str) -> Optional[Patron]:
        return self.patrons.get_patron_by_id(patron_id=patron_id)

    def search_patrons(self, criteria: PatronSearchCriteria) -> list[Patron]:
        return self.patrons.search_patrons(criteria=criteria)

    def get_patron_borrows(
        self, patron_id: str, borrow_status: BorrowStatus
    ) -> list[Borrow]:
        if borrow_status == BorrowStatus.EXPIRED:
            return self.patrons.get_patron_overdue_borrows(patron_id=patron_id)
        if borrow_status == BorrowStatus.ACTIVE:
            return self.patrons.get_patron_active_borrows(patron_id=patron_id)
        return self.patrons.get_patron_borrows(patron_id=patron_id)

    def calculate_patron_overdues_fines(self, patron_id: str) -> float:
        return self.patrons.calculate_patron_overdues_fines(patron_id=patron_id)
