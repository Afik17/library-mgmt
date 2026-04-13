from dataclasses import dataclass
from datetime import datetime

from core.exceptions.inventory import BookNotFound
from core.exceptions.patron import PatronNotFound
from entities.borrow import Borrow
from schemas.borrow import BorrowCreateRequest
from services.borrow import BorrowManager
from services.inventory import InventoryManager
from services.patron import PatronManager


@dataclass
class Library:
    """
    Orchestration object for complex operations involving multiple managers (example: for validations).

    Note: When migrating to FastAPI, this class can optionally be deprecated
    in favor of specific Use Case managers
    """

    inventory: InventoryManager
    patrons: PatronManager
    borrows: BorrowManager

    def init_borrow(self, borrow: BorrowCreateRequest) -> Borrow:
        if not self.inventory.search_books(book_id=borrow.book_id):
            raise BookNotFound(book_id=borrow.book_id)
        if not self.patrons.get_patron_by_id(patron_id=borrow.patron_id):
            raise PatronNotFound(patron_id=borrow.patron_id)
        return self.borrows.init_borrow(borrow=borrow)

    def get_patron_borrows(self, patron_id: str) -> list[Borrow]:
        if not self.patrons.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        return self.borrows.get_patron_borrows(patron_id=patron_id)

    def get_patron_active_borrows(self, patron_id: str) -> list[Borrow]:
        if not self.patrons.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        return self.borrows.get_patron_active_borrows(patron_id=patron_id)

    def get_patron_overdue_borrows(self, patron_id: str) -> list[Borrow]:
        if not self.patrons.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        active_borrows: list[Borrow] = self.get_patron_active_borrows(patron_id)
        overdue_borrows = [
            borrow for borrow in active_borrows if borrow.due_date <= datetime.now()
        ]
        return overdue_borrows

    def calculate_patron_overdues_fines(self, patron_id: str) -> float:
        if not self.patrons.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        return self.borrows.calculate_patron_overdues_fines(patron_id=patron_id)
