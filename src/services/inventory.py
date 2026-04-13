from typing import Optional
import uuid
from dataclasses import dataclass

from core.exceptions.inventory import DuplicateBook
from core.logs.base import TransactionActions, TransactionLogger
from entities.book import Book
from repositories.base import BookRepo
from schemas.book import (
    BookCreateRequest,
    BookUpdateRequest,
)


@dataclass
class InventoryManager:
    book_repo: BookRepo
    logger: TransactionLogger

    def add_book(self, book: BookCreateRequest) -> Book:
        if self.search_books(title=book.title, author=book.author):
            raise DuplicateBook(title=book.title, author=book.author)
        book_id = str(uuid.uuid4())[:8]
        new_book = Book(
            book_id=book_id, available_copies=book.total_copies, **book.model_dump()
        )
        self.book_repo.save(book=new_book)
        self.logger.record_transaction(
            action=TransactionActions.ADD_BOOK, book_id=book_id
        )
        return new_book

    def update_book(self, book_id: str, book: BookUpdateRequest) -> Book:
        updated_fields = book.model_dump(exclude_unset=True)
        updated_book: Book = self.book_repo.update(
            book_id=book_id, updated_fields=updated_fields
        )
        self.logger.record_transaction(
            action=TransactionActions.UPDATE_BOOK, book_id=book_id
        )
        return updated_book

    def remove_book(self, book_id: str) -> None:
        self.book_repo.remove(book_id=book_id)
        self.logger.record_transaction(
            action=TransactionActions.REMOVE_BOOK, book_id=book_id
        )

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        return self.book_repo.get_by_id(book_id=book_id)

    def search_books(self, **criteria) -> list[Book]:
        return self.book_repo.find_by_criteria(**criteria)
