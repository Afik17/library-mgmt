from dataclasses import asdict
from datetime import datetime

from core.config import get_settings
from core.logs.csv import CSVTransactionLogger
from models.book import Book
from models.patron import Patron
from repositories.memory import InMemoryBookRepo, InMemoryBorrowRepo, InMemoryPatronRepo
from routers.library import Library
from schemas.book import BookCreateRequest, BookUpdateRequest
from schemas.borrow import BorrowCreateRequest
from schemas.patron import PatronCreateRequest
from services.borrow import BorrowManager
from services.inventory import InventoryManager
from services.patron import PatronManager


settings = get_settings()

book_repo = InMemoryBookRepo()
patron_repo = InMemoryPatronRepo()
borrow_repo = InMemoryBorrowRepo()

logger = CSVTransactionLogger(file_path=settings.transactions_file_path)

inventory = InventoryManager(book_repo=book_repo, logger=logger)
patrons = PatronManager(repo=patron_repo, logger=logger)
borrows = BorrowManager(
    repo=borrow_repo, overdue_return_fine=settings.overdue_return_fine, logger=logger
)


library = Library(inventory=inventory, patrons=patrons, borrows=borrows)

"""" Test InventoryManager"""

books_to_add = [
    BookCreateRequest(
        title="The Site Reliability Workbook",
        author="Betsy Beyer",
        isbn="978-1492029502",
        category="DevOps",
        publish_date=datetime(2018, 7, 24),
    ),
    BookCreateRequest(
        title="Accelerate",
        author="Nicole Forsgren",
        isbn="978-1942788331",
        category="Management",
        publish_date=datetime(2018, 3, 27),
    ),
    BookCreateRequest(
        title="Kubernetes: Up and Running",
        author="Brendan Burns",
        isbn="978-1492046530",
        category="Infrastructure",
        publish_date=datetime(2019, 10, 22),
    ),
]

for book in books_to_add:
    library.inventory.add_book(book)

searched_book: Book = library.inventory.search_books(
    title="Kubernetes", category="Infrastructure"
)[0]

searched_book.author = "Dana team"
library.inventory.update_book(book=BookUpdateRequest(**asdict(searched_book)))

first_book = library.inventory.search_books(publish_date=datetime(2018, 3, 27))[0]
second_book = library.inventory.search_books(publish_date=datetime(2019, 10, 22))[0]
third_book = library.inventory.search_books(publish_date=datetime(2018, 7, 24))[0]

print("----------------------------------------------")

""" Test PatronManager"""

patrons_to_add = [
    PatronCreateRequest(
        patron_id="326228637",
        first_name="John",
        last_name="Doe",
        email="john.doe@email.com",
        phone_number="555-0101",
        birth_date=datetime(1990, 5, 15),
        membership_date=datetime.now(),
        role="regular",
        status="active",
        monthly_payment=10.0,
        discount_rate=0.0,
    ),
    PatronCreateRequest(
        patron_id="213994783",
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@university.edu",
        phone_number="555-0202",
        birth_date=datetime(2002, 11, 3),
        membership_date=datetime.now(),
        role="student",
        status="active",
        monthly_payment=5.0,
        discount_rate=0.20,
    ),
]

for patron in patrons_to_add:
    library.patrons.register_new_patron(patron=patron)

print(library.patrons.get_patrons_by_status(status="active"))
print(library.patrons.get_all())
first_patron: Patron = library.patrons.get_patron_by_name(
    first_name="Jane", last_name="smith"
)[0]
first_patron.discount_rate = 55.0
library.patrons.update_patron(patron=patron)
seconed_patron: Patron = library.patrons.get_patron_by_name(
    first_name="John", last_name="Doe"
)[0]
print("----------------------------------------------")


""" Test BorrowManager """

borrows_to_create = [
    BorrowCreateRequest(
        book_id=first_book.book_id,
        patron_id=first_patron.patron_id,
        checkout_date=datetime.now(),
        due_date=datetime(2026, 10, 4),
    ),
    BorrowCreateRequest(
        book_id=second_book.book_id,
        patron_id=seconed_patron.patron_id,
        checkout_date=datetime(2026, 4, 1),
        due_date=datetime(2027, 11, 2),
    ),
    BorrowCreateRequest(
        book_id=third_book.book_id,
        patron_id=first_patron.patron_id,
        checkout_date=datetime(2026, 3, 1),
        due_date=datetime(2026, 4, 1),
    ),
]

for borrow in borrows_to_create:
    library.borrows.init_borrow(borrow=borrow)

print(library.get_patron_overdue_borrows(patron_id=first_patron.patron_id))
print(library.borrows.get_active_borrows())
print(library.calculate_patron_overdues_fines(patron_id=seconed_patron.patron_id))
