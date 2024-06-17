from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session

from app.dependencies import get_current_active_admin
from app.schemas import AuthRequest, UserCreate, PasswordResetRequest, User
from app.models import User as UserModel
from app.database import get_db
from app.utils.enums import UserRole
from app.utils.jwt_service import jwt_service
from app.utils.security_service import security_service
from app.utils.email_service import email_service
from app.repository import UserRepository

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED, summary="Register a new user",
             responses={
                 201: {"description": "User successfully registered"},
                 400: {"description": "Email already registered"}
             })
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    - **username**: The username of the new user.
    - **password**: The password of the new user.
    - **email**: The email of the new user.
    """
    user_repo = UserRepository()
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security_service.get_password_hash(user.password)
    new_user = UserModel(username=user.username, email=user.email, password=hashed_password, role=UserRole.USER)
    user_repo.create(db, new_user)

    email_service.send_registration_email(request, user.username, user.email, user.password)
    return new_user


@router.post("/login", summary="Login a user", responses={
    200: {"description": "User successfully logged in"},
    401: {"description": "Invalid email or password"},
    403: {"description": "Account is suspended or disabled"}
})
def login(auth_request: AuthRequest, db: Session = Depends(get_db)):
    """
    Login a user.

    - **email**: The email of the user.
    - **password**: The password of the user.
    """
    user_repo = UserRepository()
    user = db.query(UserModel).filter(UserModel.email == auth_request.email).first()
    if not user or not security_service.verify_password(auth_request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if user.suspended_account:
        raise HTTPException(status_code=403, detail="Account is suspended")

    access_token = jwt_service.create_access_token(
        {"sub": user.username, "id": user.user_id, "email": user.email, "role": user.role})
    refresh_token = jwt_service.create_refresh_token(
        {"sub": user.username, "id": user.user_id, "email": user.email, "role": user.role})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", summary="Refresh the JWT token", responses={
    200: {"description": "Token successfully refreshed"},
    403: {"description": "No refresh token provided"}
})
def refresh_token(request: Request, db: Session = Depends(get_db)):
    """
    Refresh the JWT token.
    """
    refresh_token = request.headers.get("Authorization")
    if not refresh_token:
        raise HTTPException(status_code=403, detail="No refresh token provided")

    token = refresh_token.split(" ")[1]
    payload = jwt_service.verify_access_token(token)
    new_access_token = jwt_service.create_access_token(
        {"sub": payload["sub"], "id": payload["id"], "email": payload["email"], "role": payload["role"]})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/reset_password", summary="Reset user password", responses={
    200: {"description": "Password reset email sent"},
    404: {"description": "User not found"}
})
def reset_password(request: Request, password_reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Reset a user's password.

    - **email**: The email of the user requesting a password reset.
    - **new_password**: The new password provided by the user.
    """
    user_repo = UserRepository()
    user = db.query(UserModel).filter(UserModel.email == password_reset_request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = security_service.get_password_hash(password_reset_request.new_password)
    user.password = hashed_password
    user_repo.update(db, user)

    email_service.send_reset_password_email(request, user.email, password_reset_request.new_password)
    return {"msg": "Password reset email sent"}


@router.put("/enable_user/{user_id}", response_model=User, summary="Enable or disable a user account", responses={
    200: {"description": "User status updated successfully"},
    404: {"description": "User not found"}
})
def enable_user(user_id: int, enabled: bool, db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_active_admin)):
    user_repo = UserRepository()
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.suspended_account = not enabled
    user_repo.update(db, user)
    return user
