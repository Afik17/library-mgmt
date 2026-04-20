from datetime import datetime

from beanie import Document
from pydantic import Field


class PatronDoc(Document):
    patron_id: str = Field(unique=True)
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: datetime
    membership_date: datetime
    role: str
    status: str
    monthly_payment: float = Field(ge=0)
    discount_rate: float = Field(ge=0, le=100)

    class Settings:
        name = "patrons"