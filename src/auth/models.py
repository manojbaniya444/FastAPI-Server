from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from typing import List

class User(SQLModel, table=True):
    __tablename__ = "user_accounts"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"}
        )
    )
    
    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = False
    email: str
    password_hash: str = Field(exclude=True, min_length=5) # This will exclude the field when in return
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
            default=datetime.now
        )
    )
    
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"