from dataclasses import asdict
from typing import Optional

from entities.book import Book
from entities.borrow import Borrow
from entities.patron import Patron
from models.mongodb.borrow import BorrowDoc
from models.mongodb.patron import PatronDoc
from repositories.base import BookRepo, BorrowRepo, PatronRepo
from mongoengine import Document, connect, disconnect
from models.mongodb.book import BookDoc
from schemas.borrow import BorrowExtendRequest
from schemas.patron import PatronUpdateRequest


def init_db(uri: str, port: int, db: str, username: str, password: str) -> None:
    connect(db=db, host=uri, port=port, username=username, password=password)


def disconnect_db() -> None:
    disconnect(alias="default")


class MongoDBBookRepo(BookRepo):
    def _to_doc(self, book: Book) -> BookDoc:
        return BookDoc(**asdict(book))

    def _to_entity(self, book_doc: BookDoc) -> Book:
        book_dict = book_doc.to_mongo().to_dict()
        book_dict.pop("_id")
        return Book(**book_dict)

    def save(self, book: Book) -> Book:
        book_doc = self._to_doc(book=book)
        book_doc.save()
        return book

    def remove(self, book_id) -> None:
        BookDoc.objects(book_id=book_id).delete()

    def update(self, book_id: str, updated_fields: dict[str, any]) -> Book:
        updated_fields = {f"set__{key}": value for key, value in updated_fields.items()}
        updated_book: BookDoc = BookDoc.objects(book_id=book_id).modify(
            new=True, **updated_fields
        )
        return self._to_entity(book_doc=updated_book)

    def get_by_id(self, book_id) -> Optional[Book]:
        try:
            book_doc = BookDoc.objects.get(book_id=book_id)
        except BookDoc.DoesNotExist:
            return None
        return self._to_entity(book_doc=book_doc)

    def get_all(self) -> list[Book]:
        book_docs = BookDoc.objects()
        books = [self._to_entity(book) for book in book_docs]
        return books

    def find_by_criteria(self, **criteria) -> list[Book]:
        book_docs = BookDoc.objects(**criteria)
        books = [self._to_entity(book) for book in book_docs]
        return books


class MongoDBPatronRepo(PatronRepo):
    def _to_doc(self, patron: Patron) -> BookDoc:
        return PatronDoc(**asdict(patron))

    def _to_entity(self, patron_doc: PatronDoc) -> Book:
        patron_dict = patron_doc.to_mongo().to_dict()
        patron_dict.pop("_id")
        return Patron(**patron_dict)

    def save(self, patron: Patron) -> Patron:
        patron_doc: PatronDoc = self._to_doc(patron=patron)
        patron_doc.save()
        return patron

    def update(self, patron_id: str, updated_fields: dict[str, any]) -> Patron:
        updated_fields = {f"set__{key}": value for key, value in updated_fields.items()}
        updated_patron = PatronDoc.objects(patron_id=patron_id).modify(
            new=True, **updated_fields
        )
        return self._to_entity(patron_doc=updated_patron)

    def remove(self, patron_id: str) -> None:
        PatronDoc.objects(patron_id=patron_id).delete()

    def get_by_id(self, patron_id: str) -> Optional[Patron]:
        try:
            patron_doc: PatronDoc = PatronDoc.objects.get(patron_id=patron_id)
        except PatronDoc.DoesNotExist:
            return None
        return self._to_entity(patron_doc=patron_doc)

    def get_all(self) -> list[Patron]:
        patron_docs = PatronDoc.objects()
        patrons = [self._to_entity(patron) for patron in patron_docs]
        return patrons

    def find_by_criteria(self, **criteria) -> list[Patron]:
        patron_docs = PatronDoc.objects(**criteria)
        patrons = [self._to_entity(patron) for patron in patron_docs]
        return patrons


class MongoDBBorrowRepo(BorrowRepo):
    def _to_doc(self, borrow: Borrow) -> BookDoc:
        return BorrowDoc(**asdict(borrow))

    def _to_entity(self, borrow_doc: BorrowDoc) -> Book:
        borrow_dict = borrow_doc.to_mongo().to_dict()
        borrow_dict.pop("_id")
        return Borrow(**borrow_dict)

    def save(self, borrow: Borrow) -> Borrow:
        borrow_doc: BorrowDoc = self._to_doc(borrow=borrow)
        borrow_doc.save()
        return borrow

    def update(self, borrow_id: str, updated_fields: dict[str, any]) -> Borrow:
        updated_fields = {f"set__{key}": value for key, value in updated_fields.items()}
        updated_borrow: BorrowDoc = BorrowDoc.objects(borrow_id=borrow_id).modify(
            new=True, **updated_fields
        )
        return self._to_entity(borrow_doc=updated_borrow)

    def remove(self, borrow_id: str) -> None:
        BorrowDoc.objects(borrow_id=borrow_id).delete()

    def get_by_id(self, borrow_id) -> Optional[Borrow]:
        try:
            borrow_doc = BorrowDoc.objects.get(borrow_id=borrow_id)
        except BorrowDoc.DoesNotExist:
            return None
        return self._to_entity(borrow_doc=borrow_doc)

    def get_all(self) -> list[Borrow]:
        borrow_docs = BorrowDoc.objects()
        borrows = [self._to_entity(borrow) for borrow in borrow_docs]
        return borrows

    def find_by_criteria(self, **criteria) -> list[Borrow]:
        borrow_docs = BorrowDoc.objects(**criteria)
        borrows = [self._to_entity(borrow) for borrow in borrow_docs]
        return borrows
