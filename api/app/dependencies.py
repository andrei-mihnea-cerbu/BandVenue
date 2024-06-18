from fastapi import Depends, HTTPException, Request, status, Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer, SecurityScopes, HTTPBearer, \
    HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.config import settings
from app.database import get_db
from app.models import User
from app.utils.jwt_util import jwt_service

API_KEY_HEADER_NAME = "x-api-key"
API_KEY = settings.API_KEY
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)
jwt_bearer_scheme = HTTPBearer(bearerFormat="Bearer",
                               description="Name: Authorization: Bearer\n In: Header",
                               auto_error=False)


# Dependency to get the current user from JWT token
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(jwt_bearer_scheme),
                     db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt_service.verify_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user


# Dependency to get the API key
def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")


def authenticate_user(api_key: str = Depends(get_api_key), current_user: User = Depends(get_current_user)):
    return current_user
