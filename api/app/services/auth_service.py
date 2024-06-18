# app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User as UserModel
from app.schemas import UserCreate
from app.utils.enums import UserRole
from app.repository import UserRepository
from app.utils.jwt_util import jwt_service
from app.utils.security_util import security_service
from app.utils.email_util import email_service

user_repo = UserRepository()


def register_new_user(request, user: UserCreate, db: Session):
    db_user = db.query(UserModel).filter(user.email == UserModel.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security_service.get_password_hash(user.password)
    new_user = UserModel(username=user.username, email=user.email, password=hashed_password, role=UserRole.USER)
    user_repo.create(db, new_user)

    email_service.send_registration_email(request, user.username, user.email, user.password)

    # Create access and refresh tokens
    access_token = jwt_service.create_access_token(
        {"id": new_user.user_id, "username": new_user.username, "email": new_user.email})
    refresh_token = jwt_service.create_refresh_token(
        {"id": new_user.user_id, "username": new_user.username, "email": new_user.email})

    return {"user": new_user, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


def login_user(auth_request, db: Session):
    user = db.query(UserModel).filter(UserModel.email == auth_request.email).first()
    if not user or not security_service.verify_password(auth_request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if user.suspended_account:
        raise HTTPException(status_code=403, detail="Account is suspended")

    # Create access and refresh tokens
    access_token = jwt_service.create_access_token({"id": user.user_id, "username": user.username, "email": user.email})
    refresh_token = jwt_service.create_refresh_token(
        {"id": user.user_id, "username": user.username, "email": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


def refresh_access_token(refresh_token: str, db: Session):
    try:
        payload = jwt_service.verify_refresh_token(refresh_token)
        user_id = payload.get("id")
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Create a new access token
        access_token = jwt_service.create_access_token(
            {"id": user.user_id, "username": user.username, "email": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as _:
        raise HTTPException(status_code=401, detail="Invalid token")


def reset_user_password(email: str, new_password: str, db: Session):
    user = db.query(UserModel).filter(email == UserModel.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = security_service.get_password_hash(new_password)
    user.password = hashed_password
    db.commit()
    email_service.send_reset_password_email(user.email)
    return {"msg": "Password reset successfully"}


def delete_user(user_id: int, db: Session):
    user = db.query(UserModel).filter(user_id == UserModel.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"msg": "User deleted successfully"}


def disable_user(user_id: int, enabled: bool, db: Session):
    user = db.query(UserModel).filter(user_id == UserModel.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.suspended_account = not enabled
    db.commit()
    return {"msg": "User status updated successfully"}


def modify_user(user_id: int, update_data: dict, db: Session):
    user = db.query(UserModel).filter(user_id == UserModel.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in update_data.items():
        if hasattr(user, key):
            if key == "password":
                value = security_service.get_password_hash(value)
                setattr(user, key, value)
            else:
                setattr(user, key, value)

    db.commit()
    return user
