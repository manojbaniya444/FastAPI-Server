from pydantic import BaseModel
import uuid
from typing import Optional

class BookSchema(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    user_uid: str
    
class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
    
class BookCreateModel(BaseModel):
    """
    This class is used to validate the request when creating or updating a book
    """
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str