from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from .service import UserService
from .schemas import UserModel

from src.errors import (
    InvalidTokenException,
    RefreshTokenRequiredException,
    AccessTokenRequiredException,
    InsufficientPermissionException
)

from typing import List, Any

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        # get the token in auth header automatically
        token = creds.credentials

        token_data = self.token_valid(token)
        
        
        if not token_data:
            raise InvalidTokenException()
            
        if await token_in_blocklist(token_data["jti"]):
            raise InvalidTokenException()
            
        self.verify_token_data(token_data)
        
        return token_data
    
    def token_valid(self, token: str) -> bool | dict:
        token_data = decode_token(token)

        return False if not token_data else token_data
        
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in inherit class.")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # If the refresh field is True, then it is for refresh token
        if token_data and token_data["refresh"]:
            raise AccessTokenRequiredException()
            
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Check if there if it is for refresh token or not
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequiredException()
            
async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user: UserModel = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        
        raise InsufficientPermissionException()