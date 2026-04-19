from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class BookStatus(StrEnum):
    DAMAGED = "damaged"
    AVAILABLE = "available"
    BUSY = "busy"


class Book(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    description: Optional[str] = ""
    language: Optional[str] = "English"
    publish_date: datetime
    status: Optional[BookStatus] = BookStatus.AVAILABLE


class BookCreate(Book):
    pass


class BookResponse(Book):
    book_id: str


class BookUpdate(Book):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    publish_date: Optional[datetime] = None
    status: Optional[BookStatus] = None


class BookSearchCriteria(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None


class BookBorrow(BaseModel):
    patron_id: str
    due_date: datetime
    checkout_date: Optional[datetime] = datetime.now()


class BookBorrowResponse(BookBorrow):
    borrow_id: str
    return_date: Optional[datetime] = None

class BookExtendBorrow(BaseModel):
    days: int = Field(min=1)