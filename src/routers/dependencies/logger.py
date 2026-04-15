from typing import Annotated

from fastapi import Depends

from src.core.logs.base import TransactionLogger
from src.core.logs.csv import CSVTransactionLogger
from src.core.config import Settings, get_settings


def get_transaction_logger(
    settings: Annotated[Settings, Depends(get_settings)],
) -> TransactionLogger:
    return CSVTransactionLogger(file_path=settings.transactions_file_path)
