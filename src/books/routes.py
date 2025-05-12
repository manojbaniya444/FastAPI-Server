from fastapi import status
from fastapi import APIRouter
from fastapi import HTTPException

from src.books.book_data import books
from src.books.schemas import BookSchema, BookUpdateModel

from typing import List

book_router = APIRouter()

# Returns all the books (GET)
@book_router.get("/books", response_model=List[BookSchema])
async def get_all_books():
    return books

# Post a new book (POST)
@book_router.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookSchema) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

# Return a single book (GET)
@book_router.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book with given id not found hai")

# Update a book (PATCH)
@book_router.patch("/book/{book_id}")
async def update_book(book_id: int, book_data: BookUpdateModel):
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_data.title
            book["publisher"] = book_data.publisher
            book["page_count"] = book_data.page_count
            book["language"] = book_data.language
            
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book with the given id not found hai in data")

# Delete a book in book list (DELETE)
@book_router.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            
            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")