from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Optional


class TransactionActions(StrEnum):
    ADD_BOOK = "add_book"
    REMOVE_BOOK = "remove_book"
    UPDATE_BOOK = "update_book"
    BORROW_BOOK = "borrow_book"
    RETURN_BOOK = "return_book"
    EXTEND_BORROW_BOOK = "extend_borrow_book"

    REGISTER_PATRON = "register_patron"
    UPDATE_PATRON = "update_patron"
    REMOVE_PATRON = "remove_patron"


class TransactionLogger(ABC):
    @abstractmethod
    def record_transaction(
        self,
        action: TransactionActions,
        patron_id: Optional[str] = None,
        book_id: Optional[str] = None,
        borrow_id: Optional[str] = None,
    ) -> None:
        pass
