from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Patron(ABC):
    id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: datetime
    membership_date: datetime
    category: str  # student/teacher/
    status: str  # active/expired/suspended
    payment: float
    fines: float
