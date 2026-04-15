from src.repositories.base import BorrowRepo
from src.repositories.mongodb import MongoDBBorrowRepo


def get_borrow_repo() -> BorrowRepo:
    return MongoDBBorrowRepo()