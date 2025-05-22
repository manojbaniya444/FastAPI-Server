from pydantic import BaseModel
import uuid
from typing import Optional, List
from src.reviews.schemas import ReviewModel
from src.tags.schemas import TagModel

class BookSchema(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID]
    reviews: List[ReviewModel] = []
    tags: List[TagModel] = []
    
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