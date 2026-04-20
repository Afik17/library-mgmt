from datetime import datetime
from typing import Optional

from beanie import Document

from pydantic import Field


class BorrowDoc(Document):
    borrow_id: str = Field(unique=True)
    book_id: str
    patron_id: str
    checkout_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None

    class Settings:
        name = "borrows"