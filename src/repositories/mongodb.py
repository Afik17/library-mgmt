from dataclasses import asdict
from typing import Generic, Optional, Type, TypeVar

from src.entities.book import Book
from src.entities.borrow import Borrow
from src.entities.patron import Patron
from src.models.mongodb.book import BookDoc
from src.models.mongodb.borrow import BorrowDoc
from src.models.mongodb.patron import PatronDoc
from src.repositories.base import Repository

T = TypeVar("T")  # Entity type
U = TypeVar("U")  # Document type


class MongoRepo(Repository[T], Generic[T, U]):
    def __init__(self, entity_class: Type[T], doc_class: Type[U], id_field: str = "id"):
        self.entity_class = entity_class
        self.doc_class = doc_class
        self.id_field = id_field

    def _to_doc(self, entity: T) -> U:
        return self.doc_class(**asdict(entity))

    def _to_entity(self, doc: U) -> T:
        doc_dict = doc.model_dump()
        doc_dict.pop("id", None)
        return self.entity_class(**doc_dict)

    async def save(self, entity: T) -> T:
        doc = self._to_doc(entity=entity)
        await doc.insert()
        return entity

    async def update(self, entity_id: str, updated_fields: dict[str, any]) -> T:
        doc = await self.doc_class.find_one({self.id_field: entity_id})
        if doc is None:
            raise ValueError(f"Document with {self.id_field}={entity_id} not found")
        await doc.set(updated_fields)
        return self._to_entity(doc=doc)

    async def remove(self, entity_id: str) -> None:
        doc = await self.doc_class.find_one({self.id_field: entity_id})
        await doc.delete()

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        doc = await self.doc_class.find_one({self.id_field: entity_id})
        return self._to_entity(doc=doc) if doc else None

    async def get_all(self) -> list[T]:
        docs = await self.doc_class.find_all().to_list()
        return [self._to_entity(doc) for doc in docs]

    async def find_by_criteria(self, **criteria) -> list[T]:
        docs = await self.doc_class.find(criteria).to_list()
        return [self._to_entity(doc) for doc in docs]


class BookMongoRepo(MongoRepo[Book, BookDoc]):
    def __init__(self):
        super().__init__(entity_class=Book, doc_class=BookDoc, id_field="book_id")


class PatronMongoRepo(MongoRepo[Patron, PatronDoc]):
    def __init__(self):
        super().__init__(entity_class=Patron, doc_class=PatronDoc, id_field="patron_id")


class BorrowMongoRepo(MongoRepo[Borrow, BorrowDoc]):
    def __init__(self):
        super().__init__(entity_class=Borrow, doc_class=BorrowDoc, id_field="borrow_id")
