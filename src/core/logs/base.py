from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Optional


class TransactionActions(StrEnum):
    ADD_BOOK = "add_book"
    REMOVE_BOOK = "remove_book"
    UPDATE_BOOK = "update_book"

    REGISTER_PATRON = "register_patron"
    UPDATE_PATRON = "update_patron"
    REMOVE_PATRON = "remove_patron"

    INIT_BORROW = "init_borrow"
    END_BORROW = "end_borrow"
    EXTEND_BORROW = "extend_borrow"


class TransactionLogger(ABC):
    @abstractmethod
    def record_transaction(
        self,
        action: TransactionActions,
        patron_id: Optional[str] = None,
        book_id: Optional[str] = None,
        borrow_id: Optional[str] = None
    ) -> None:
        pass
