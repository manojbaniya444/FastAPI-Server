from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserCreateModel(BaseModel):
    username: str = Field(max_length=40)
    email: str = Field(max_length=44)
    password: str = Field(max_length=10)
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    role: UserRole = Field(default=UserRole.user)
    
class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    first_name: str
    last_name: str
    is_verified: bool
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime
    role: str