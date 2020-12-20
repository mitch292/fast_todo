from databases import DatabaseURL
from starlette.config import Config


VERSION = "0.0.0"
config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

PROJET_NAME: str = config("PROJECT_NAME", default="FastAPI Application")