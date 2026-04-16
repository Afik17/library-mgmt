from typing import Annotated

from fastapi import Depends

from src.entities.borrow import Borrow
from src.entities.patron import Patron
from src.core.config import Settings, get_settings
from src.core.logs.base import TransactionLogger
from src.repositories.base import Repository
from src.repositories.mongodb import PatronMongoRepo
from src.routers.dependencies.borrow import get_borrow_repo
from src.routers.dependencies.logger import get_transaction_logger
from src.services.patron import PatronManager


def get_patron_repo() -> Repository[Patron]:
    return PatronMongoRepo()


def get_patron_manager(
    patron_repo: Annotated[Repository[Patron], Depends(get_patron_repo)],
    borrow_repo: Annotated[Repository[Borrow], Depends(get_borrow_repo)],
    logger: Annotated[TransactionLogger, Depends(get_transaction_logger)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> PatronManager:
    return PatronManager(
        patron_repo=patron_repo,
        borrow_repo=borrow_repo,
        overdue_return_fine=settings.overdue_return_fine,
        logger=logger,
    )
