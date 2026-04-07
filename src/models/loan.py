from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Loan:
    loan_id: str
    book_id: str
    patron_id: str
    checkout_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None 