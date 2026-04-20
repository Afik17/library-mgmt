from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, entity_id: str, updated_fields: dict[str, any]) -> T:
        pass

    @abstractmethod
    async def remove(self, entity_id: str) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def find_by_criteria(self, **criteria) -> list[T]:
        pass
