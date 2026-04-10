from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    description: Optional[str] = "No desc provided"
    language: Optional[str] = "English"
    publish_date: datetime


class BookCreateRequest(Book):
    pass


class BookCreateResponse(Book):
    book_id: str


class BookUpdateRequest(Book):
    book_id: str
    pass


class BookUpdateResponse(Book):
    pass
