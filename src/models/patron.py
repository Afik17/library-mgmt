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
    role: str  # regular/student/teacher
    status: str  # active/expired/suspended
    fines: float
    monthly_payment: float
    discount_rate: float

    def get_total_payment(self) -> float:
        return self.monthly_payment * (self.discount_rate // 100) + self.fines


@dataclass
class TeacherPatron(Patron):
    discount_rate: float


@dataclass
class StudentPatron(Patron):
    discount_rate: float
