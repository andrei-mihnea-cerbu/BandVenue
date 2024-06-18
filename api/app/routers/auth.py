# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.dependencies import get_db
from app.schemas.user import AuthRequest, UserCreate, PasswordResetRequest, UserUpdateRequest, Token
from app.services.auth_service import (
    register_new_user, login_user, refresh_access_token,
    reset_user_password, delete_user, disable_user, modify_user
)
from app.utils.jwt_util import jwt_service

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED, summary="Register a new user",
             responses={
                 201: {"description": "User successfully registered and JWT tokens provided."},
                 400: {"description": "Invalid data or email already registered."}
             })
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with a username, email, and password.
    This endpoint will also send an email verification message.
    """
    return register_new_user(request, user, db)


@router.post("/login", response_model=Token, summary="Login a user",
             responses={
                 200: {"description": "User logged in successfully with access and refresh tokens returned."},
                 401: {"description": "Incorrect email or password."},
                 403: {"description": "Account is suspended or disabled."}
             })
def login(auth_request: AuthRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and provide JWT tokens if successful.
    """
    return login_user(auth_request, db)


@router.post("/refresh", response_model=Token, summary="Refresh the JWT token",
             responses={
                 200: {"description": "Access token successfully refreshed."},
                 403: {"description": "Invalid or no refresh token provided."}
             })
def refresh_token(request: Request, refresh_token: str = Depends(jwt_service.verify_refresh_token),
                  db: Session = Depends(get_db)):
    """
    Refresh an expired access token using a valid refresh token.
    """
    return refresh_access_token(request, refresh_token, db)


@router.post("/reset_password", summary="Reset user password",
             responses={
                 200: {"description": "Password reset successfully. A confirmation email has been sent."},
                 404: {"description": "User not found with provided email."}
             })
def reset_password(password_reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Allow a user to reset their password, requiring their email and new password.
    Sends a confirmation email upon successful reset.
    """
    return reset_user_password(password_reset_request.email, password_reset_request.new_password, db)


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a user from the database.
    """
    delete_user(user_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/disable/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def disable_user_endpoint(user_id: int, enabled: bool, db: Session = Depends(get_db)):
    """
    Enable or disable a user account based on the boolean 'enabled' parameter.
    """
    disable_user(user_id, enabled, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/modify/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def modify_user_endpoint(user_id: int, update_request: UserUpdateRequest, db: Session = Depends(get_db)):
    """
    Update user details such as username, email, and potentially other profile information.
    """
    modify_user(user_id, update_request.dict(exclude_unset=True), db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
