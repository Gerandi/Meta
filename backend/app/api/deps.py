# backend/app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core import security
from app.db.session import get_db
from app.models.user import User
from app.services import user_service
from app import schemas # Import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") # Matches the login endpoint with /auth prefix

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = security.decode_token(token)
    if user_id is None:
        raise credentials_exception
    try:
        user_id_int = int(user_id)
    except ValueError:
         raise credentials_exception # If user_id is not an int
    user = user_service.get_user(db, user_id=user_id_int)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not user_service.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
