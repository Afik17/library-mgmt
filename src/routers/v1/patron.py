from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from src.routers.dependencies.library import get_library
from src.schemas.borrow import BorrowFine, BorrowResponse, BorrowStatus
from src.schemas.patron import (
    PatronCreate,
    PatronResponse,
    PatronSearchCriteria,
    PatronUpdate,
)
from src.services.library import Library

router = APIRouter(prefix="/patrons", tags=["Patrons"])


@router.get("/{patron_id}", response_model=Optional[PatronResponse])
async def get_patron_by_id(
    patron_id: str, library: Annotated[Library, Depends(get_library)]
) -> Optional[PatronResponse]:
    return await library.get_patron_by_id(patron_id=patron_id)


@router.get("", response_model=list[PatronResponse])
async def search_patrons(
    library: Annotated[Library, Depends(get_library)],
    criteria: PatronSearchCriteria = Depends(),
) -> list[PatronResponse]:
    return await library.search_patrons(criteria=criteria)


@router.get("/{patron_id}/borrows", response_model=list[BorrowResponse])
async def get_patron_borrows(
    patron_id: str,
    library: Annotated[Library, Depends(get_library)],
    borrow_status: Optional[BorrowStatus] = None,
) -> list[BorrowResponse]:
    return await library.get_patron_borrows(patron_id=patron_id, borrow_status=borrow_status)


@router.get("/{patron_id}/borrows/fines", response_model=BorrowFine)
async def calculate_patron_overdues_fines(
    patron_id: str,
    library: Annotated[Library, Depends(get_library)],
) -> float:
    total_fines = await library.calculate_patron_overdues_fines(patron_id=patron_id)
    return BorrowFine(total_fines=total_fines)


@router.post("", response_model=PatronResponse, status_code=status.HTTP_201_CREATED)
async def register_new_patron(
    patron: PatronCreate, library: Annotated[Library, Depends(get_library)]
) -> PatronResponse:
    return await library.register_new_patron(patron=patron)


@router.patch("/{patron_id}", response_model=PatronResponse)
async def update_patron(
    patron_id: str,
    patron: PatronUpdate,
    library: Annotated[Library, Depends(get_library)],
) -> PatronResponse:
    return await library.update_patron(patron_id=patron_id, patron=patron)


@router.delete(
    "/{patron_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_patron(
    patron_id: str,
    library: Annotated[Library, Depends(get_library)],
) -> None:
    await library.remove_patron(patron_id=patron_id)
