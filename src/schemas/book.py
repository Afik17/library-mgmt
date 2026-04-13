from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    description: Optional[str] = ""
    language: Optional[str] = "English"
    publish_date: datetime
    total_copies: int = Field(min=0, default=0)


class BookCreateRequest(Book):
    pass


class BookCreateResponse(Book):
    book_id: str


class BookUpdateRequest(Book):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    publish_date: Optional[datetime] = None
    total_copies: int = Field(min=0, default=None)
    available_copies: int = Field(min=0, default=None)


class BookUpdateResponse(Book):
    book_id: str
