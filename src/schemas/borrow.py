from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Borrow(BaseModel):
    book_id: str
    patron_id: str
    checkout_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None


class BorrowCreateRequest(Borrow):
    pass


class BorrowCreateResponse(Borrow):
    borrow_id: str


class BorrowUpdateRequest(Borrow):
    pass


class BorrowUpdateResponse(Borrow):
    borrow_id: str
