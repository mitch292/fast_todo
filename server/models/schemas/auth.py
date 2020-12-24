from uuid import UUID
from typing import Optional

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInCreate(BaseModel):
    username: str
    password: str
    is_disabled: bool = False
    full_name: Optional[str] = None

class UserInDB(UserInCreate):
    id: UUID
    hashed_password: str

class UserInUpdate(BaseModel):
    id: UUID
    username: str
    password: str
    is_disabled: bool = False
    full_name: Optional[str] = None