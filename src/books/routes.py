from fastapi import status
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from src.books.book_data import books
from src.books.schemas import BookSchema, BookUpdateModel, BookCreateModel
from src.books.service import BookService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer
from src.auth.dependencies import RoleChecker

from typing import List

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker_admin = Depends(RoleChecker(["admin"]))
role_checker_user = Depends(RoleChecker(["user","admin"]))

# Returns all the books (GET)
# Set the dependencies in the http call
@book_router.get("/", response_model=List[BookSchema], dependencies=[role_checker_user])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
):
    books = await book_service.get_all_books(session)
    return books

# Post a new book (POST)
@book_router.post("/", status_code=status.HTTP_201_CREATED,  dependencies = [role_checker_admin])
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_uid=user_id, session=session)
    # TODO: Any nice to do here why?
    return new_book.model_dump()

# Return a single book (GET)
@book_router.get("/{book_uuid}", dependencies = [role_checker_user])
async def get_book(
    book_uuid: str,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
) -> dict:
    book = await book_service.get_book(book_uuid, session)
    
    if book:
        # TODO: Here also
        return book.model_dump()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book with given id not found hai")

# Update a book (PATCH)
@book_router.patch("/{book_uuid}", dependencies=[role_checker_admin])
async def update_book(
    book_uuid: str,
    book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
):
    updated_book = await book_service.update_book(book_uuid, book_data, session)
        
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book with the given id not found hai in data")
    else:
        return updated_book

# Delete a book in book list (DELETE)
@book_router.delete("/{book_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(
    book_uuid: str,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _: bool = Depends(RoleChecker(["admin"])) # checks the role to be admin to delete the book from the database
):
    book_to_delete = await book_service.delete_book(book_uuid, session)
    
    if book_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return {}