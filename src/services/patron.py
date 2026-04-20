from datetime import datetime
from typing import Optional

from src.repositories.base import Repository
from src.core.exceptions.patron import DuplicatePatron, PatronNotFound
from src.core.logs.base import TransactionActions, TransactionLogger
from src.entities.borrow import Borrow
from src.entities.patron import Patron, StudentPatron, TeacherPatron
from src.schemas.patron import PatronCreate, PatronSearchCriteria, PatronUpdate


class PatronManager:
    def __init__(
        self,
        patron_repo: Repository[Patron],
        borrow_repo: Repository[Borrow],
        overdue_return_fine: float,
        logger: TransactionLogger,
    ):

        self.patron_repo: Repository = patron_repo
        self.borrow_repo: Repository = borrow_repo
        self.overdue_return_fine: float = overdue_return_fine
        self._roles = {
            "regular": self._create_regular,
            "student": self._create_student,
            "teacher": self._create_teacher,
        }
        self.logger: TransactionLogger = logger

    async def _create_regular(self, patron: PatronCreate) -> Patron:
        patron = Patron(**patron.model_dump())
        await self.patron_repo.save(patron)
        return patron

    async def _create_student(self, patron: PatronCreate) -> Patron:
        patron = StudentPatron(**patron.model_dump())
        await self.patron_repo.save(patron)
        return patron

    async def _create_teacher(self, patron: PatronCreate) -> Patron:
        patron = TeacherPatron(**patron.model_dump())
        await self.patron_repo.save(patron)
        return patron

    async def register_new_patron(self, patron: PatronCreate) -> Patron:
        if await self.get_patron_by_id(patron_id=patron.patron_id):
            raise DuplicatePatron(patron_id=patron.patron_id)
        patron_based_role = self._roles.get(patron.role)
        self.logger.record_transaction(
            action=TransactionActions.REGISTER_PATRON,
            patron_id=patron.patron_id,
        )
        return await patron_based_role(patron)

    async def update_patron(self, patron_id: str, patron: PatronUpdate) -> Patron:
        if not await self.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        updated_fields = patron.model_dump(exclude_unset=True)
        updated_patron = await self.patron_repo.update(
            entity_id=patron_id, updated_fields=updated_fields
        )
        self.logger.record_transaction(
            action=TransactionActions.UPDATE_PATRON,
            patron_id=patron_id,
        )
        return updated_patron

    async def remove_patron(self, patron_id: str) -> None:
        if not await self.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        await self.patron_repo.remove(entity_id=patron_id)
        self.logger.record_transaction(
            action=TransactionActions.REMOVE_PATRON,
            patron_id=patron_id,
        )

    async def get_patron_by_id(self, patron_id: str) -> Optional[Patron]:
        return await self.patron_repo.get_by_id(entity_id=patron_id)

    async def search_patrons(self, criteria: PatronSearchCriteria) -> list[Patron]:
        return await self.patron_repo.find_by_criteria(
            **criteria.model_dump(exclude_none=True)
        )

    async def get_patron_borrows(self, patron_id: str) -> list[Borrow]:
        if not await self.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        return await self.borrow_repo.find_by_criteria(patron_id=patron_id)

    async def get_patron_active_borrows(self, patron_id: str) -> list[Borrow]:
        if not await self.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        return await self.borrow_repo.find_by_criteria(patron_id=patron_id, return_date=None)

    async def get_patron_overdue_borrows(self, patron_id: str) -> list[Borrow]:
        if not await self.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        active_borrows: list[Borrow] = await self.get_patron_active_borrows(patron_id)
        overdue_borrows = [
            borrow for borrow in active_borrows if borrow.due_date <= datetime.now()
        ]
        return overdue_borrows

    async def calculate_patron_overdues_fines(self, patron_id: str) -> float:
        if not await self.get_patron_by_id(patron_id=patron_id):
            raise PatronNotFound(patron_id=patron_id)
        overdue_borrows = await self.get_patron_overdue_borrows(patron_id=patron_id)
        return len(overdue_borrows) * self.overdue_return_fine
