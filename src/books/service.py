from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel
import sqlmodel
from datetime import datetime
import uuid
from sqlalchemy.orm import selectinload

class BookService:
    """
    This class provides methods to create, read, update and delete book
    """
    async def get_all_books(self, session: AsyncSession):
        """
        Get a list of all books
        
        Returns:
            list: list of books
        """
        statement = sqlmodel.select(Book).order_by(sqlmodel.desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def create_book(self, book_data: BookCreateModel, user_uid: uuid.UUID, session: AsyncSession):
        """
        Create a new book
        
        Args:
            book_data (BookSchema): data to create a new
            
        Returns:
            Book: the new book
        """
        book_data_dict = book_data.model_dump()
        
        # new_book.published_date = datetime.strftime(book_data.published_date, "%Y-%m-%d") 
        # get this type of date: "2020-01-05"
        
        new_book = Book(
            **book_data_dict
        )
        
        new_book.user_uid = user_uid
        
        session.add(new_book)
        
        await session.commit()
        
        return new_book
    
    async def get_user_books(self, user_uid: uuid.UUID, session: AsyncSession):
        # get the book with user_uid equal to the user_uid provided match (get books of user)
        statement = (
            sqlmodel.select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(sqlmodel.desc(Book.created_at))
        )
        
        result = await session.exec(statement)
        
        return result.all()
    
    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession):
        """
        Get a book by its UUID
        
        Args:
            book_uuid (str) : the UUID of the book
            
        Returns:
            Book: the book object
        """
        statement = sqlmodel.select(Book).where(Book.uid == book_uid).options(
            selectinload(Book.reviews),
            selectinload(Book.tags)
        )
        result = await session.exec(statement)
        
        book = result.first()
        
        return book if book is not None else None
    
    async def update_book(self, book_uid: uuid.UUID, update_data: BookUpdateModel, session: AsyncSession):
        """
        Update a book
        
        Args:
            book_uid (str): the UUID of the book
            update_data (BookCreateModel): the data to update the book
            
        Returns:
            Book: the updated book
        """
        
        book_to_update = await self.get_book(book_uid, session)
        
        if book_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            
            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)
                
            await session.commit()
            
            return book_to_update
        
        else:
            return None
        
    async def delete_book(self, book_uuid: uuid.UUID, session: AsyncSession):
        """
        Delete a book
        
        Args:
            book_uid (str): the UUID of the book
        """
        book_to_delete = await self.get_book(book_uuid, session)
        
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            
            await session.commit()
            
            return {}
        
        else:
            return None
        