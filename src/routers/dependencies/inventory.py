from typing import Annotated

from fastapi import Depends

from src.entities.borrow import Borrow
from src.entities.book import Book
from src.core.logs.base import TransactionLogger
from src.repositories.base import Repository
from src.repositories.mongodb import BookMongoRepo
from src.routers.dependencies.borrow import get_borrow_repo
from src.routers.dependencies.logger import get_transaction_logger
from src.services.inventory import InventoryManager


def get_inventory_repo() -> Repository[Book]:
    return BookMongoRepo()


def get_inventory_manager(
    book_repo: Annotated[Repository[Book], Depends(get_inventory_repo)],
    borrow_repo: Annotated[Repository[Borrow], Depends(get_borrow_repo)],
    logger: Annotated[TransactionLogger, Depends(get_transaction_logger)],
) -> InventoryManager:
    return InventoryManager(book_repo=book_repo, borrow_repo=borrow_repo, logger=logger)
