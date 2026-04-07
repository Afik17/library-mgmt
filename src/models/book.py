from dataclasses import dataclass
from datetime import datetime


@dataclass
class Book:
    id: str
    title: str
    author: str
    isbn: str
    category: str
    description: str
    language: str
    release_date: datetime