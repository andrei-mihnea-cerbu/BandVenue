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

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT"))
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS").lower() in ['true', '1', 't']
    MAIL_FROM: str = os.getenv("MAIL_FROM")


settings = Settings()
