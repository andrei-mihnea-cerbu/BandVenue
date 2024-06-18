from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.user import AuthRequest, UserCreate, PasswordResetRequest, Token
from app.services import auth_service_class
from app.utils.jwt_util import jwt_service

router = APIRouter()


@router.post("/register",
             response_model=Token,
             status_code=status.HTTP_201_CREATED,
             summary="Register a new user",
             responses={
                 201: {
                     "description": "User successfully registered and JWT tokens provided.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "username": "newuser",
                                 "email": "newuser@example.com",
                                 "password": "strongpassword123",
                                 "role": "User"
                             }
                         }
                     }
                 },
                 400: {
                     "description": "Email already registered.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Email already registered."
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             })
def register(request: Request, user: UserCreate):
    """
    Register a new user with a username, email, and password.
    This endpoint will also send an email verification message.
    """
    return auth_service_class.register_new_user(request, user)


@router.post("/login",
             include_in_schema=True,
             response_model=Token,
             summary="Login a user",
             responses={
                 200: {
                     "description": "User logged in successfully with access and refresh tokens returned.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                 "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                 "token_type": "bearer"
                             }
                         }
                     }
                 },
                 401: {
                     "description": "Incorrect email or password.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid email or password."
                             }
                         }
                     }
                 },
                 403: {
                     "description": "Account is suspended.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Account is suspended."
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             })
def login(auth_request: AuthRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and provide JWT tokens if successful.
    """
    return auth_service_class.login_user(auth_request, db)


@router.post("/refresh",
             response_model=Token,
             summary="Refresh the JWT token",
             responses={
                 200: {
                     "description": "Access token successfully refreshed.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                 "token_type": "bearer"
                             }
                         }
                     }
                 },
                 403: {
                     "description": "Invalid or no refresh token provided.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Authorization header missing"
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             })
def refresh_token(refresh_token: str = Depends(jwt_service.verify_refresh_token),
                  db: Session = Depends(get_db)):
    """
    Refresh an expired access token using a valid refresh token.
    """
    return auth_service_class.refresh_access_token(refresh_token, db)


@router.post("/reset_password",
             summary="Reset user password",
             responses={
                 200: {
                     "description": "Password reset successfully. A confirmation email has been sent.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Password reset successfully"
                             }
                         }
                     }
                 },
                 404: {
                     "description": "User not found with provided email.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "User not found"
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Invalid data.",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid body format"
                             }
                         }
                     }
                 }
             })
def reset_password(password_reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Allow a user to reset their password, requiring their email and new password.
    Sends a confirmation email upon successful reset.
    """
    return auth_service_class.reset_user_password(password_reset_request.email, password_reset_request.new_password, db)

