from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status

class AppException(Exception):
    """Base class for all the app errors."""
    pass

class InvalidTokenException(AppException):
    """User has provided an invalid or expired token."""
    pass

class RevokedTokenException(AppException):
    """User has provided a token that has been revoked."""
    pass

class AccessTokenRequiredException(AppException):
    """User has provided a refresh token when an access token is needed."""
    pass

class RefreshTokenRequiredException(AppException):
    """User has provided an access token when a refresh token is needed."""
    pass

class UserAlreadyExistsException(AppException):
    """User has provided an email for a user who exists during sign up."""
    pass

class InvalidCredentialsException(AppException):
    """User has provided wrong email or password during log in."""
    pass

class InsufficientPermissionException(AppException):
    """User does not have the necessary permissions to perform an action."""
    pass

class BookNotFoundException(AppException):
    """Book not found."""
    pass

class TagNotFoundException(AppException):
    """Tag not found."""
    pass

class TagAlreadyExistsException(AppException):
    """Tag already exists."""
    pass

class UserNotFoundException(AppException):
    """User not found."""
    pass

def create_exception_handler(
    status_code: int,
    initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
    return exception_handler

def register_error_handlers(app: FastAPI):
    """Register all the error handlers for our app."""
    app.add_exception_handler(
        UserAlreadyExistsException,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists please use different email.",
                "error_code": "user_exists"
            }
        )
    )
    
    app.add_exception_handler(
        UserNotFoundException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User with given email not found use different.",
                "error_code": "user_not_found"
            }
        )
    )
    
    app.add_exception_handler(
        BookNotFoundException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "user_not_found"
            }
        )
    )
    
    
    app.add_exception_handler(
        InvalidCredentialsException,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidTokenException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedTokenException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequiredException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequiredException,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermissionException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
    app.add_exception_handler(
        TagNotFoundException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Tag Not Found", "error_code": "tag_not_found"},
        ),
    )

    app.add_exception_handler(
        TagAlreadyExistsException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Tag Already exists",
                "error_code": "tag_exists",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFoundException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book Not Found",
                "error_code": "book_not_found",
            },
        ),
    )
    
    @app.exception_handler(500)
    async def internal_server_error(request, exception):
        return JSONResponse(
            content={
                "message": "Oops! something went wrong in our server.",
                "error_code": "server_error"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )