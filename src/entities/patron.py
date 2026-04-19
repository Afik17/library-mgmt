from dataclasses import dataclass
from datetime import datetime


@dataclass
class Patron:
    patron_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: datetime
    membership_date: datetime
    role: str
    status: str
    monthly_payment: float
    discount_rate: float


@dataclass
class TeacherPatron(Patron):
    pass


@dataclass
class StudentPatron(Patron):
    pass
