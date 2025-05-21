from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel, Field

from .schemas import UserCreateModel, UserModel, UserBooksModel
from .service import UserService
from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from .utils import create_access_token, verify_password
from src.config import Config 
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker

auth_router = APIRouter()
user_service = UserService()
role_checker_admin = RoleChecker(["admin"])
role_checker_user = RoleChecker(["user"])
class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=5)

@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
    ):
    email = user_data.email
    
    user_exists = await user_service.user_exists(email, session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with given email already exists")
    
    new_user = await user_service.create_user(user_data, session)
    
    return new_user

@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user_by_email(email, session)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email."
        )

    password_valid = verify_password(password, user.password_hash)
    
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
        )
        
    access_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)}
    )
            
    refresh_token = create_access_token(
        user_data={"email": user.email, "user_uid": str(user.uid)},
        refresh=True,
        expiry=timedelta(days=Config.REFRESH_TOKEN_EXPIRY)
    )
            
    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "uid": str(user.uid)
            }
        }
    )
    
@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(user=Depends(get_current_user), _: bool = Depends(role_checker_admin)):
    return user

@auth_router.get("/refresh_token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer())
):
    expiry_timestamp = token_details["exp"]
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        # create a new access token if the refresh token has not expired yet.
        new_access_token = create_access_token(
            user_data=token_details["user"]
        )
        return JSONResponse(
            content={"access_token": new_access_token}
        )
        
    raise HTTPException(
        status=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired Refresh Token Login."
    )
    
@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    
    await add_jti_to_blocklist(jti=jti)
    
    return JSONResponse(
        content={
            "message": "Logged out successfully."
        },
        status_code=status.HTTP_200_OK
    )