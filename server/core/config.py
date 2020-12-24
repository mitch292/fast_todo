from databases import DatabaseURL
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette.config import Config

VERSION = "0.0.0"
config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)

PROJET_NAME: str = config("PROJECT_NAME", default="FastAPI Application")

SECRET_KEY = config("SECRET_KEY", cast=str)
ALGORITHM = config("ALGORITHM", cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth/token/")
