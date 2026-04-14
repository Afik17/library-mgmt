import csv
import os
import uuid
from datetime import datetime
from typing import Optional

from src.core.logs.base import TransactionActions, TransactionLogger


class CSVTransactionLogger(TransactionLogger):
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.file_headers = [
            "transaction_id",
            "action",
            "date",
            "patron_id",
            "book_id",
            "borrow_id",
            "description",
        ]

        self._ensure_file_exists()

    def _ensure_file_exists(self):
        file_exists = os.path.isfile(self.file_path)

        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.file_headers)
            if not file_exists:
                writer.writeheader()

    def record_transaction(
        self,
        action: TransactionActions,
        patron_id: Optional[str] = None,
        book_id: Optional[str] = None,
        borrow_id: Optional[str] = None,
    ) -> None:
        transaction_id = str(uuid.uuid4())[:8]
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "transaction_id": transaction_id,
            "action": action,
            "date": current_date,
            "patron_id": patron_id,
            "book_id": book_id,
            "borrow_id": borrow_id,
        }
        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.file_headers)
            writer.writerow(record)
