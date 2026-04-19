from src.entities.borrow import Borrow
from src.repositories.base import Repository
from src.repositories.mongodb import BorrowMongoRepo


def get_borrow_repo() -> Repository[Borrow]:
    return BorrowMongoRepo()
