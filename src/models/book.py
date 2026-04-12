from dataclasses import dataclass
from datetime import datetime


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    isbn: str
    category: str
    description: str
    language: str
    publish_date: datetime