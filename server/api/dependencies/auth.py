from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from api.errors import invalid_credentials_exception
from core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    OAUTH2_SCHEME,
    PWD_CONTEXT,
    SECRET_KEY,
)
from db.db import database, users
from db.repositories.auth import UserRepository
from models.schemas.auth import TokenData, UserInCreate, UserInDB, UserInResponse


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches the hashed password."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Return a hashed version of a plain text password."""
    return PWD_CONTEXT.hash(password)


async def get_user(username: str) -> UserInDB:
    """Return a user from the database for a given username."""
    query = users.select().where(username == users.c.username)
    user_row = await database.fetch_one(query=query)

    if not user_row:
        raise invalid_credentials_exception
    return UserInDB(**user_row)


async def authenticate_user(username: str, password: str) -> Union[bool, UserInDB]:
    """Attempt to authenticate a given username and password"""
    user = await get_user(username)
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
    user = await get_user(username=token_data.username)  # type: ignore
    if user is None:
        raise invalid_credentials_exception
    return user


async def get_current_active_user(
    current_user: UserInResponse = Depends(get_current_user),
):
    """For a given JWT token, get the active user."""
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
