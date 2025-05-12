from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List

from data import books

app = FastAPI()

# schema for our body parameter book
class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    
# schema for our body book update
class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    
# route to get all the books
@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books

# create a new book
@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    # convert the pydantic ovject to the python dict format
    new_book = book_data.model_dump()
    books.append(new_book)
    return {
        "message": "New book added to the list",
        "new_book": new_book
    }
    
# get the book by id
@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# remove the book by id
@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            
            return {"message": "success deletion book in list"}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found in the database")

# update the book
@app.patch("/book/{book_id}")
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    # look book and then update
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language
            book["author"] = book_update_data.author
            
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")