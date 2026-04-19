from dataclasses import asdict
from typing import Generic, Optional, Type, TypeVar

from mongoengine import connect, disconnect

from src.entities.book import Book
from src.entities.borrow import Borrow
from src.entities.patron import Patron
from src.models.mongodb.book import BookDoc
from src.models.mongodb.borrow import BorrowDoc
from src.models.mongodb.patron import PatronDoc
from src.repositories.base import Repository

T = TypeVar("T")  # Entity type
U = TypeVar("U")  # Document type


def init_db(uri: str, port: int, db: str, username: str, password: str) -> None:
    connect(db=db, host=uri, port=port, username=username, password=password)


def disconnect_db() -> None:
    disconnect(alias="default")


class MongoRepo(Repository[T], Generic[T, U]):
    def __init__(self, entity_class: Type[T], doc_class: Type[U], id_field: str = "id"):
        self.entity_class = entity_class
        self.doc_class = doc_class
        self.id_field = id_field

    def _to_doc(self, entity: T) -> U:
        return self.doc_class(**asdict(entity))

    def _to_entity(self, doc: U) -> T:
        doc_dict = doc.to_mongo().to_dict()
        doc_dict.pop("_id")
        return self.entity_class(**doc_dict)

    def save(self, entity: T) -> T:
        doc = self._to_doc(entity=entity)
        doc.save()
        return entity

    def update(self, entity_id: str, updated_fields: dict[str, any]) -> T:
        updated_fields = {f"set__{key}": value for key, value in updated_fields.items()}
        updated_doc = self.doc_class.objects(**{self.id_field: entity_id}).modify(
            new=True, **updated_fields
        )
        return self._to_entity(doc=updated_doc)

    def remove(self, entity_id: str) -> None:
        self.doc_class.objects(**{self.id_field: entity_id}).delete()

    def get_by_id(self, entity_id: str) -> Optional[T]:
        try:
            doc = self.doc_class.objects.get(**{self.id_field: entity_id})
        except self.doc_class.DoesNotExist:
            return None
        return self._to_entity(doc=doc)

    def get_all(self) -> list[T]:
        docs = self.doc_class.objects()
        return [self._to_entity(doc) for doc in docs]

    def find_by_criteria(self, **criteria) -> list[T]:
        docs = self.doc_class.objects(**criteria)
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
