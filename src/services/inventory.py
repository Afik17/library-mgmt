import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Optional

from src.core.exceptions.inventory import (
    BookNotBorrowed,
    BookNotFound,
    BookUnavailable,
)
from src.core.logs.base import TransactionActions, TransactionLogger
from src.entities.book import Book
from src.entities.borrow import Borrow
from src.repositories.base import BookRepo, BorrowRepo
from src.schemas.book import (
    BookBorrow,
    BookCreate,
    BookSearchCriteria,
    BookStatus,
    BookUpdate,
)


@dataclass
class InventoryManager:
    book_repo: BookRepo
    borrow_repo: BorrowRepo
    logger: TransactionLogger

    def add_book(self, book: BookCreate) -> Book:
        book_id = str(uuid.uuid4())[:8]
        new_book = Book(book_id=book_id, **book.model_dump())
        self.book_repo.save(book=new_book)
        self.logger.record_transaction(
            action=TransactionActions.ADD_BOOK, book_id=book_id
        )
        return new_book

    def update_book(self, book_id: str, book: BookUpdate) -> Book:
        if not self.get_book_by_id(book_id=book_id):
            raise BookNotFound(book_id=book_id)
        updated_fields = book.model_dump(exclude_unset=True)
        updated_book: Book = self.book_repo.update(
            book_id=book_id, updated_fields=updated_fields
        )
        self.logger.record_transaction(
            action=TransactionActions.UPDATE_BOOK, book_id=book_id
        )
        return updated_book

    def remove_book(self, book_id: str) -> None:
        if not self.get_book_by_id(book_id=book_id):
            raise BookNotFound(book_id=book_id)
        self.book_repo.remove(book_id=book_id)
        self.logger.record_transaction(
            action=TransactionActions.REMOVE_BOOK, book_id=book_id
        )

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        return self.book_repo.get_by_id(book_id=book_id)

    def search_books(self, criteria: BookSearchCriteria) -> list[Book]:
        search_criteria = criteria.model_dump(exclude_none=True)
        return self.book_repo.find_by_criteria(**search_criteria)

    def get_borrow_by_book(self, book_id: str) -> Borrow:
        return self.borrow_repo.find_by_criteria(book_id=book_id)[0]

    def borrow_book(self, book_id: str, book_borrow: BookBorrow) -> Borrow:
        book: Book = self.get_book_by_id(book_id=book_id)
        if not book:
            raise BookNotFound(book_id=book_id)
        if book.status != BookStatus.AVAILABLE:
            raise BookUnavailable(book_id=book_id)
        book.status = BookStatus.BUSY
        self.update_book(book_id=book_id, book=BookUpdate(**asdict(book)))
        borrow_id = str(uuid.uuid4())[:8]
        new_borrow = Borrow(
            borrow_id=borrow_id,
            book_id=book_id,
            return_date=None,
            **book_borrow.model_dump(),
        )
        self.borrow_repo.save(borrow=new_borrow)
        self.logger.record_transaction(
            action=TransactionActions.RETURN_BOOK,
            book_id=book_id,
            patron_id=book_borrow.patron_id,
            borrow_id=borrow_id,
        )
        return new_borrow

    def extend_borrow_book(self, book_id: str, days: int) -> Borrow:
        book: Book = self.get_book_by_id(book_id=book_id)
        if not book:
            raise BookNotFound(book_id=book_id)
        borrow: Borrow = self.get_borrow_by_book(book_id=book_id)
        if not borrow or book.status == BookStatus.AVAILABLE:
            raise BookNotBorrowed(book_id=book_id)
        new_due_date = borrow.due_date + timedelta(days=days)
        updated_borrow = self.borrow_repo.update(
            borrow_id=borrow.borrow_id, updated_fields={"due_date": new_due_date}
        )
        return updated_borrow

    def return_book(self, book_id: str) -> Borrow:
        book: Book = self.get_book_by_id(book_id=book_id)
        if not book:
            raise BookNotFound(book_id=book_id)
        borrow: Borrow = self.get_borrow_by_book(book_id=book_id)
        if not borrow or book.status != BookStatus.BUSY:
            raise BookNotBorrowed(book_id=book_id)
        returned_borrow = self.borrow_repo.update(
            borrow_id=borrow.borrow_id, updated_fields={"return_date": datetime.now()}
        )
        book.status = BookStatus.AVAILABLE
        self.update_book(book_id=book_id, book=BookUpdate(**asdict(book)))
        self.logger.record_transaction(
            action=TransactionActions.RETURN_BOOK,
            book_id=borrow.book_id,
            patron_id=borrow.patron_id,
            borrow_id=borrow.borrow_id,
        )
        return returned_borrow
