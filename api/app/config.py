from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    API_KEY: str = os.getenv("API_KEY")
    MODE: str = os.getenv("MODE")

    POSTGRESQL_URL: str = os.getenv("POSTGRESQL_URL")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY")
    MAIL_FROM: str = os.getenv("MAIL_FROM")


settings = Settings()
