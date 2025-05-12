from fastapi import FastAPI

from src.books.routes import book_router
from src.db.main import initdb

from contextlib import asynccontextmanager

version = "v1"

# the lifespan event manager in fastapi app server data
# this will run once at the start before yield and then after closing
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is Starting")
    await initdb()
    yield
    print("Server is Stopping")

# Instantiate the FastAPI application here
app = FastAPI(
    title="Book API",
    description="A Backend API for book web app",
    version=version,
    lifespan=lifespan
)

# Include the books_router here
app.include_router(
    book_router,
    prefix=f"/api/{version}",
    tags=["books"]
)