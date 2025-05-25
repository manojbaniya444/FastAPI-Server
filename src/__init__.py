from fastapi import FastAPI

from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tag_router
from src.errors import register_error_handlers
from src.db.main import initdb
from src.middleware import register_middleware

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
    # lifespan=lifespan
)

# register error handler here
register_error_handlers(app)

# register middleware here
register_middleware(app)

# Include the books_router here
app.include_router(
    book_router,
    prefix=f"/api/{version}/books",
    tags=["books"]
)

app.include_router(
    auth_router,
    prefix=f"/api/{version}/auth",
    tags=["auth"]
)

app.include_router(
    review_router,
    prefix=f"/api/{version}/reviews",
    tags=["reviews"]
)

app.include_router(
    tag_router,
    prefix=f"/api/{version}/tags",
    tags=["tags"]
)