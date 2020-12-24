from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.schemas.auth import UserInCreate, UserInDB, Token
from db.repositories.auth import UserRepository
from api.dependencies.auth import get_current_active_user, authenticate_user

router = APIRouter()

@router.get("/users/me/", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user

@router.get("/users/", response_model=List[UserInDB])
async def list_users(users_repo=Depends(UserRepository)):
    return await users_repo.get_all_users()


@router.post("/users/", response_model=UserInDB)
async def register_user(new_user: UserInCreate, users_repo=Depends(UserRepository)):
    return await users_repo.create_user(new_user)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}