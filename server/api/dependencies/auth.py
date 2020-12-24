from typing import Optional, Union
from datetime import datetime, timedelta

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext

from models.schemas.auth import UserInDB, UserInCreate
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, PWD_CONTEXT, OAUTH2_SCHEME
from api.errors import invalid_credentials_exception

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches the hashed password."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Return a hashed version of a plain text password."""
    return PWD_CONTEXT.hash(password)

def get_user(username: str) -> UserInDB:
    """Return a user from the database for a given username."""
    # TODO this will probably move somewhere else
    return UserInDB(**user_dict)

def authenticate_user(username: str, password: str) -> Union[bool, UserInDB]:
    """Attempt to authenticate a given username and password"""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# TODO: Type the return
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create an encoded JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(OAUTH2_SCHEME)) -> UserInDB:
    """For a given JWT token, get the user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise invalid_credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise invalid_credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise invalid_credentials_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """For a given JWT token, get the active user."""
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user