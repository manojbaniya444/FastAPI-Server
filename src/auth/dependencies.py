from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

from .utils import decode_token
from src.db.redis import token_in_blocklist

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        # get the token in auth header automatically
        token = creds.credentials

        token_data = self.token_valid(token)
        
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been revoked.",
                    "resolution": "Please login again."
                }
            )
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get a new token"
                }
            )
            
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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token."
            )
            
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Check if there if it is for refresh token or not
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token."
            )