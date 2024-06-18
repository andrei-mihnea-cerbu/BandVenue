from pydantic import BaseModel, EmailStr
from app.utils.enums import UserRole


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: str = UserRole.USER


class User(UserBase):
    user_id: int
    role: str
    suspended_account: bool

    class Config:
        from_attributes = True


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr
    new_password: str


class UserUpdateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
