import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.core.exceptions.borrow import BorrowNotFound
from src.core.logs.base import TransactionActions, TransactionLogger
from src.entities.borrow import Borrow
from src.repositories.base import BorrowRepo
from src.schemas.borrow import BorrowCreateRequest


@dataclass
class BorrowManager:
    repo: BorrowRepo
    overdue_return_fine: float
    logger: TransactionLogger

    def init_borrow(self, borrow: BorrowCreateRequest) -> Borrow:
        borrow_id = str(uuid.uuid4())[:8]
        new_borrow = Borrow(borrow_id=borrow_id, **borrow.model_dump())
        self.repo.save(new_borrow)
        self.logger.record_transaction(
            action=TransactionActions.INIT_BORROW,
            book_id=borrow.book_id,
            patron_id=borrow.patron_id,
            borrow_id=borrow_id,
        )
        return new_borrow

    def extend_borrow_period(self, borrow_id: str, days: int) -> Borrow:
        borrow = self.get_borrow_by_id(borrow_id=borrow_id)
        if not borrow:
            raise BorrowNotFound(borrow_id=borrow_id)
        new_due_date = borrow.due_date + timedelta(days=days)
        updated_borrow = self.repo.update(
            borrow_id=borrow_id, updated_fields={"due_date": new_due_date}
        )
        self.logger.record_transaction(
            action=TransactionActions.EXTEND_BORROW,
            book_id=borrow.book_id,
            patron_id=borrow.patron_id,
            borrow_id=borrow.borrow_id,
        )
        return updated_borrow

    def end_borrow(self, borrow_id: str) -> Borrow:
        borrow = self.get_borrow_by_id(borrow_id=borrow_id)
        if not borrow:
            raise BorrowNotFound(borrow_id=borrow_id)
        updated_fields = {"return_date": datetime.now()}
        updated_borrow = self.repo.update(
            borrow_id=borrow_id, updated_fields=updated_fields
        )
        self.logger.record_transaction(
            action=TransactionActions.END_BORROW,
            book_id=borrow.book_id,
            patron_id=borrow.patron_id,
            borrow_id=borrow_id,
        )
        return updated_borrow

    def get_borrow_by_id(self, borrow_id: str) -> Borrow:
        return self.repo.get_by_id(borrow_id)

    def get_patron_borrows(self, patron_id: str) -> list[Borrow]:
        return self.repo.find_by_criteria(patron_id=patron_id)

    def get_patron_active_borrows(self, patron_id: str) -> list[Borrow]:
        return self.repo.find_by_criteria(return_date=None, patron_id=patron_id)

    def get_patron_overdue_borrows(self, patron_id: str) -> list[Borrow]:
        active_borrows: list[Borrow] = self.get_patron_active_borrows(patron_id)
        overdue_borrows = [
            borrow for borrow in active_borrows if borrow.due_date <= datetime.now()
        ]
        return overdue_borrows

    def get_active_borrows(self) -> list[Borrow]:
        return self.repo.find_by_criteria(return_date=None)

    def get_all(self) -> list[Borrow]:
        return self.repo.get_all()

    def calculate_patron_overdues_fines(self, patron_id: str) -> float:
        overdue_borrows = self.get_patron_overdue_borrows(patron_id=patron_id)
        return len(overdue_borrows) * self.overdue_return_fine
