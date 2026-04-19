from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class PatronRole(StrEnum):
    REGULAR = "regular"
    STUDENT = "student"
    TEACHER = "teacher"


class PatronStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class Patron(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: datetime
    membership_date: datetime
    role: PatronRole
    status: PatronStatus
    monthly_payment: float = Field(min=0)
    discount_rate: float = Field(min=0, max=100)


class PatronCreate(Patron):
    patron_id: str


class PatronUpdate(Patron):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    birth_date: Optional[datetime] = None
    membership_date: Optional[datetime] = None
    role: Optional[PatronRole] = None
    status: Optional[PatronStatus] = None
    monthly_payment: float = Field(min=0, default=None)
    discount_rate: float = Field(min=0, max=100, default=None)


class PatronResponse(Patron):
    patron_id: str


class PatronSearchCriteria(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    role: Optional[PatronRole] = None
    status: Optional[PatronStatus] = None