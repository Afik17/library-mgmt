from fastapi import APIRouter

from .book import router as book_router
from .patron import router as patron_router


def initialize_v1_router() -> APIRouter:
    v1_router = APIRouter(prefix="/v1")
    v1_router.include_router(book_router)
    v1_router.include_router(patron_router)
    return v1_router
