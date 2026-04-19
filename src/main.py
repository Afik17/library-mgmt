from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.config import get_settings
from src.core.exceptions.base import LibraryError
from src.repositories.mongodb import disconnect_db, init_db
from src.routers.v1.router import initialize_v1_router

settings = get_settings()

app = FastAPI(
    title="Library management", description="Organize and manage your favorite library"
)


# Future use with adync ODM beanie
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     init_db(
#         uri=settings.mongodb.uri,
#         port=settings.mongodb.port,
#         db=settings.mongodb.db,
#         username=settings.mongodb.username,
#         password=settings.mongodb.password,
#     )
#     yield
#     disconnect_db()


@app.on_event("startup")
async def startup_event():
    init_db(
        uri=settings.mongodb.uri,
        port=settings.mongodb.port,
        db=settings.mongodb.db,
        username=settings.mongodb.username,
        password=settings.mongodb.password,
    )


@app.on_event("shutdown")
async def shutdown_event():
    disconnect_db()


v1_router = initialize_v1_router()

app.include_router(v1_router)


@app.exception_handler(LibraryError)
async def unicorn_exception_handler(request: Request, exc: LibraryError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.msg})
