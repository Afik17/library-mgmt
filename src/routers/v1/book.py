from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from src.core.security import RoleVerifier
from src.schemas.auth import Role
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

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[
        Depends(RoleVerifier(allowed_roles=[Role.LIBRARIAN]))
    ],
)


@router.get(
    "/{book_id}",
    response_model=Optional[BookResponse],
)
async def get_book_id(
    book_id: str,
    library: Annotated[Library, Depends(get_library)],
) -> BookResponse:
    return await library.get_book_by_id(book_id=book_id)


@router.get("", response_model=list[BookResponse])
async def search_books(
    library: Annotated[Library, Depends(get_library)],
    criteria: BookSearchCriteria = Depends(),
) -> BookResponse:
    return await library.search_books(criteria=criteria)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_book(
    book: BookCreate,
    library: Annotated[Library, Depends(get_library)],
):
    return await library.add_book(book=book)


@router.post("/{book_id}/borrow", response_model=BookBorrowResponse)
async def borrow_book(
    book_id: str,
    book_borrow: BookBorrow,
    library: Annotated[Library, Depends(get_library)],
) -> BookBorrow:
    return await library.borrow_book(book_id=book_id, book_borrow=book_borrow)


@router.patch("/{book_id}/borrow", response_model=BookBorrowResponse)
async def extend_borrow_book(
    book_id: str,
    extend_borrow_book: BookExtendBorrow,
    library: Annotated[Library, Depends(get_library)],
) -> BookBorrowResponse:
    return await library.extend_borrow_book(
        book_id=book_id, days=extend_borrow_book.days
    )


@router.patch("/{book_id}/return", response_model=BookBorrowResponse)
async def return_book(
    book_id: str, library: Annotated[Library, Depends(get_library)]
) -> BookBorrowResponse:
    return await library.return_book(book_id=book_id)


@router.patch("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: str,
    book: BookUpdate,
    library: Annotated[Library, Depends(get_library)],
) -> BookResponse:
    return await library.update_book(book_id=book_id, book=book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book(
    book_id: str,
    library: Annotated[Library, Depends(get_library)],
) -> None:
    return await library.remove_book(book_id=book_id)
