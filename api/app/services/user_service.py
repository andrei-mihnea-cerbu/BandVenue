# app/services/user_service.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.utils.security_util import security_service


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def delete_user(self, user_id: int):
        user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.db.delete(user)
        self.db.commit()
        return {"msg": "User deleted successfully"}

    def disable_user(self, user_id: int, enabled: bool):
        user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.suspended_account = not enabled
        self.db.commit()
        return {"msg": "User status updated successfully"}

    def modify_user(self, user_id: int, update_data: dict):
        user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in update_data.items():
            if hasattr(user, key):
                if key == "password":
                    value = security_service.get_password_hash(value)
                    setattr(user, key, value)
                else:
                    setattr(user, key, value)

        self.db.commit()
        return user
