from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class BorrowStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"


class Borrow(BaseModel):
    book_id: str
    patron_id: str
    checkout_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None


class BorrowCreate(Borrow):
    pass


class BorrowCreateResponse(Borrow):
    borrow_id: str


class BorrowExtendRequest(BaseModel):
    days: int


class BorrowResponse(Borrow):
    borrow_id: str


class BorrowFine(BaseModel):
    total_fines: float = Field(min=0)