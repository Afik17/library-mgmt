from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, EmailStr


class PatronRole(StrEnum):
    REGULAR = "regular"
    STUDENT = "student"
    TEACHER = "teacher"


class PatronStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class Patron(BaseModel):
    patron_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: datetime
    membership_date: datetime
    role: PatronRole
    status: PatronStatus
    monthly_payment: float
    discount_rate: float


class PatronCreateRequest(Patron):
    pass


class PatronCreateResponse(Patron):
    pass
