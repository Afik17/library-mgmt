from datetime import datetime

from beanie import Document
from pydantic import Field


class BookDoc(Document):
    book_id: str = Field(unique=True)
    title: str
    author: str
    isbn: str
    category: str
    description: str
    language: str
    publish_date: datetime
    status: str

    class Settings:
        name = "books"
