from typing import Optional

from core.logs.base import TransactionActions, TransactionLogger
from entities.patron import Patron, StudentPatron, TeacherPatron
from repositories.base import PatronRepo
from schemas.patron import PatronCreateRequest, PatronUpdateRequest


class PatronManager:
    def __init__(self, repo: PatronRepo, logger: TransactionLogger):

        self.repo: PatronRepo = repo
        self._roles = {
            "regular": self._create_regular,
            "student": self._create_student,
            "teacher": self._create_teacher,
        }
        self.logger: TransactionLogger = logger

    def _create_regular(self, patron: PatronCreateRequest) -> Patron:
        patron = Patron(**patron.model_dump())
        self.repo.save(patron)
        return patron

    def _create_student(self, patron: PatronCreateRequest) -> Patron:
        patron = StudentPatron(**patron.model_dump())
        self.repo.save(patron)
        return patron

    def _create_teacher(self, patron: PatronCreateRequest) -> Patron:
        patron = TeacherPatron(**patron.model_dump())
        self.repo.save(patron)
        return patron

    def register_new_patron(self, patron: PatronCreateRequest) -> Patron:
        patron_based_role = self._roles.get(patron.role)
        self.logger.record_transaction(
            action=TransactionActions.REGISTER_PATRON,
            patron_id=patron.patron_id,
        )
        return patron_based_role(patron)

    def update_patron(self, patron_id: str, patron: PatronUpdateRequest) -> Patron:
        updated_fields = patron.model_dump(exclude_unset=True)
        updated_patron = self.repo.update(
            patron_id=patron_id, updated_fields=updated_fields
        )
        self.logger.record_transaction(
            action=TransactionActions.UPDATE_PATRON,
            patron_id=patron_id,
        )
        return updated_patron

    def remove_patron(self, patron_id: str) -> None:
        self.repo.remove(patron_id=patron_id)
        self.logger.record_transaction(
            action=TransactionActions.REMOVE_PATRON,
            patron_id=patron_id,
        )

    def get_patron_by_id(self, patron_id: str) -> Optional[Patron]:
        return self.repo.get_by_id(patron_id)

    def get_patron_by_name(self, first_name: str, last_name: str) -> list[Patron]:
        return self.repo.find_by_criteria(first_name=first_name, last_name=last_name)

    def get_patrons_by_status(self, status: str) -> list[Patron]:
        return self.repo.find_by_criteria(status=status)

    def get_all(self) -> list[Patron]:
        return self.repo.get_all()
