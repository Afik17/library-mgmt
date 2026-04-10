from dataclasses import dataclass

from models.book import Book
from schemas.book import BookCreateRequest, BookCreateResponse, BookUpdateRequest, BookUpdateResponse

from .borrow import BorrowManager
from .inventory import InventoryManager
from .patron import PatronManager


@dataclass
class Library:
    inventory: InventoryManager
    patrons: PatronManager
    borrows: BorrowManager
    
