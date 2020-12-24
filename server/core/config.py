from databases import DatabaseURL
from starlette.config import Config

VERSION = "0.0.0"
config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)

PROJET_NAME: str = config("PROJECT_NAME", default="FastAPI Application")
