from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class BaseUser(BaseModel):
    username: str
    full_name: Optional[str] = None
    is_disabled: bool = False


class UserInCreate(BaseUser):
    password: str


class UserInResponse(BaseUser):
    id: UUID


class UserInDB(BaseUser):
    id: UUID
    hashed_password: str


class UserInUpdate(BaseModel):
    id: UUID
    username: str
    password: str
    is_disabled: bool = False
    full_name: Optional[str] = None
