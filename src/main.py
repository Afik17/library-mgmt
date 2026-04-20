from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from motor import motor_asyncio

from src.models.mongodb.user import UserDoc
from src.core.config import get_settings
from src.core.exceptions.base import LibraryError
from src.models.mongodb.book import BookDoc
from src.models.mongodb.borrow import BorrowDoc
from src.models.mongodb.patron import PatronDoc
from src.routers.v1.router import initialize_v1_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    full_uri = f"mongodb://{settings.mongodb.username}:{settings.mongodb.password}@{settings.mongodb.uri}:{settings.mongodb.port}"
    client = motor_asyncio.AsyncIOMotorClient(full_uri)
    await init_beanie(
        database=client[settings.mongodb.db],
        document_models=[BookDoc, PatronDoc, BorrowDoc, UserDoc],
    )
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Library management",
    description="Organize and manage your favorite library",
)

v1_router = initialize_v1_router()

app.include_router(v1_router)


@app.exception_handler(LibraryError)
async def library_exception_handler(request: Request, exc: LibraryError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.msg})
