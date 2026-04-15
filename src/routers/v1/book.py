from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from src.routers.dependencies.library import get_library
from src.schemas.book import (
    BookBorrow,
    BookBorrowResponse,
    BookCreate,
    BookExtendBorrow,
    BookResponse,
    BookSearchCriteria,
    BookUpdate,
)
from src.services.library import Library

router = APIRouter(prefix="/books", tags=["Books"])


@router.get(
    "/{book_id}",
    response_model=Optional[BookResponse],
)
def get_book_id(
    book_id: str,
    library: Annotated[Library, Depends(get_library)],
) -> BookResponse:
    return library.get_book_by_id(book_id=book_id)


@router.get("", response_model=list[BookResponse])
def search_books(
    library: Annotated[Library, Depends(get_library)],
    criteria: BookSearchCriteria = Depends(),
) -> BookResponse:
    return library.search_books(criteria=criteria)


@router.post("", status_code=status.HTTP_201_CREATED)
def add_book(
    book: BookCreate,
    library: Annotated[Library, Depends(get_library)],
):
    return library.add_book(book=book)


@router.post("/{book_id}/borrow", response_model=BookBorrowResponse)
def borrow_book(
    book_id: str,
    book_borrow: BookBorrow,
    library: Annotated[Library, Depends(get_library)],
) -> BookBorrow:
    return library.borrow_book(book_id=book_id, book_borrow=book_borrow)


@router.patch("/{book_id}/borrow", response_model=BookBorrowResponse)
def extend_borrow_book(
    book_id: str,
    extend_borrow_book: BookExtendBorrow,
    library: Annotated[Library, Depends(get_library)],
) -> BookBorrowResponse:
    return library.extend_borrow_book(book_id=book_id, days=extend_borrow_book.days)


@router.patch("/{book_id}/return", response_model=BookBorrowResponse)
def return_book(
    book_id: str, library: Annotated[Library, Depends(get_library)]
) -> BookBorrowResponse:
    return library.return_book(book_id=book_id)


@router.patch("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: str,
    book: BookUpdate,
    library: Annotated[Library, Depends(get_library)],
) -> BookResponse:
    return library.update_book(book_id=book_id, book=book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_book(
    book_id: str,
    library: Annotated[Library, Depends(get_library)],
) -> None:
    return library.remove_book(book_id=book_id)
