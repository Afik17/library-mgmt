import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Optional

from src.repositories.base import Repository
from src.core.exceptions.inventory import (
    BookNotBorrowed,
    BookNotFound,
    BookUnavailable,
)
from src.core.logs.base import TransactionActions, TransactionLogger
from src.entities.book import Book
from src.entities.borrow import Borrow
from src.schemas.book import (
    BookBorrow,
    BookCreate,
    BookSearchCriteria,
    BookStatus,
    BookUpdate,
)


@dataclass
class InventoryManager:
    book_repo: Repository[Book]
    borrow_repo: Repository[Borrow]
    logger: TransactionLogger

    async def add_book(self, book: BookCreate) -> Book:
        book_id = str(uuid.uuid4())[:8]
        new_book = Book(book_id=book_id, **book.model_dump())
        await self.book_repo.save(entity=new_book)
        self.logger.record_transaction(
            action=TransactionActions.ADD_BOOK, book_id=book_id
        )
        return new_book

    async def update_book(self, book_id: str, book: BookUpdate) -> Book:
        if not await self.get_book_by_id(book_id=book_id):
            raise BookNotFound(book_id=book_id)
        updated_fields = book.model_dump(exclude_unset=True)
        updated_book: Book = await self.book_repo.update(
            entity_id=book_id, updated_fields=updated_fields
        )
        self.logger.record_transaction(
            action=TransactionActions.UPDATE_BOOK, book_id=book_id
        )
        return updated_book

    async def remove_book(self, book_id: str) -> None:
        if not await self.get_book_by_id(book_id=book_id):
            raise BookNotFound(book_id=book_id)
        await self.book_repo.remove(entity_id=book_id)
        self.logger.record_transaction(
            action=TransactionActions.REMOVE_BOOK, book_id=book_id
        )

    async def get_book_by_id(self, book_id: str) -> Optional[Book]:
        return await self.book_repo.get_by_id(entity_id=book_id)

    async def search_books(self, criteria: BookSearchCriteria) -> list[Book]:
        search_criteria = criteria.model_dump(exclude_none=True)
        return await self.book_repo.find_by_criteria(**search_criteria)

    async def get_borrow_by_book(self, book_id: str) -> Borrow:
        try:
            return await self.borrow_repo.find_by_criteria(book_id=book_id)[0]
        except IndexError:
            raise BookNotBorrowed(book_id=book_id)

    async def borrow_book(self, book_id: str, book_borrow: BookBorrow) -> Borrow:
        book: Book = await self.get_book_by_id(book_id=book_id)
        if not book:
            raise BookNotFound(book_id=book_id)
        if book.status != BookStatus.AVAILABLE:
            raise BookUnavailable(book_id=book_id)
        book.status = BookStatus.BUSY
        await self.update_book(book_id=book_id, book=BookUpdate(**asdict(book)))
        borrow_id = str(uuid.uuid4())[:8]
        new_borrow = Borrow(
            borrow_id=borrow_id,
            book_id=book_id,
            return_date=None,
            **book_borrow.model_dump(),
        )
        await self.borrow_repo.save(entity=new_borrow)
        self.logger.record_transaction(
            action=TransactionActions.RETURN_BOOK,
            book_id=book_id,
            patron_id=book_borrow.patron_id,
            borrow_id=borrow_id,
        )
        return new_borrow

    async def extend_borrow_book(self, book_id: str, days: int) -> Borrow:
        book: Book = await self.get_book_by_id(book_id=book_id)
        if not book:
            raise BookNotFound(book_id=book_id)
        borrow: Borrow = await self.get_borrow_by_book(book_id=book_id)
        if not borrow or book.status == BookStatus.AVAILABLE:
            raise BookNotBorrowed(book_id=book_id)
        new_due_date = borrow.due_date + timedelta(days=days)
        updated_borrow = await self.borrow_repo.update(
            entity_id=borrow.borrow_id, updated_fields={"due_date": new_due_date}
        )
        return updated_borrow

    async def return_book(self, book_id: str) -> Borrow:
        book: Book = await self.get_book_by_id(book_id=book_id)
        if not book:
            raise BookNotFound(book_id=book_id)
        borrow: Borrow = await self.get_borrow_by_book(book_id=book_id)
        if book.status != BookStatus.BUSY:
            raise BookNotBorrowed(book_id=book_id)
        returned_borrow = await self.borrow_repo.update(
            entity_id=borrow.borrow_id, updated_fields={"return_date": datetime.now()}
        )
        book.status = BookStatus.AVAILABLE
        await self.update_book(book_id=book_id, book=BookUpdate(**asdict(book)))
        self.logger.record_transaction(
            action=TransactionActions.RETURN_BOOK,
            book_id=borrow.book_id,
            patron_id=borrow.patron_id,
            borrow_id=borrow.borrow_id,
        )
        return returned_borrow
