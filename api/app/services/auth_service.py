from jose import JWTError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User as UserModel
from app.schemas import UserCreate
from app.utils.enums import UserRole
from app.utils.jwt_util import jwt_service
from app.utils.security_util import security_service
from app.utils.email_util import email_service


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_new_user(self, request, user: UserCreate):
        db_user = self.db.query(UserModel).filter(user.email == UserModel.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = security_service.get_password_hash(user.password)
        new_user = UserModel(username=user.username, email=user.email, password=hashed_password, role=UserRole.USER)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        email_service.send_registration_email(request, user.username, user.email, user.password)
        return {"user": new_user}

    def login_user(self, auth_request):
        user = self.db.query(UserModel).filter(UserModel.email == auth_request.email).first()
        if not user or not security_service.verify_password(auth_request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if user.suspended_account:
            raise HTTPException(status_code=403, detail="Account is suspended")

        # Create access and refresh tokens
        access_token = jwt_service.create_access_token({"id": user.user_id, "username": user.username, "email": user.email})
        refresh_token = jwt_service.create_refresh_token(
            {"id": user.user_id, "username": user.username, "email": user.email})

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    def refresh_access_token(self, refresh_token: str):
        try:
            payload = jwt_service.verify_refresh_token(refresh_token)
            user_id = payload.get("id")
            user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Create a new access token
            access_token = jwt_service.create_access_token(
                {"id": user.user_id, "username": user.username, "email": user.email})
            return {"access_token": access_token, "token_type": "bearer"}

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def reset_user_password(self, email: str, new_password: str):
        user = self.db.query(UserModel).filter(email == UserModel.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        hashed_password = security_service.get_password_hash(new_password)
        user.password = hashed_password
        self.db.commit()
        email_service.send_reset_password_email(user.email)
        return {"detail": "Password reset successfully"}