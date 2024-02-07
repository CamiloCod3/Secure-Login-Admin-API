from dotenv import load_dotenv
load_dotenv()  # Load environment variables from the .env file

from pydantic_settings import BaseSettings
from pydantic import EmailStr
from typing import List

class Settings(BaseSettings):
    # Essential JWT settings
    secret_key: str
    algorithm: str = "HS256"  # Adding algorithm here for JWT operations
    access_token_expires_delta: int = 30  # Expires in 30 minutes
    refresh_token_expires_delta: int = 1440  # Expires in 24 hours (1440 minutes)

    # Admin user configuration
    admin_email: EmailStr
    admin_password: str
    admin_name: str = 'Admin'  # Default admin name, override if necessary

    # Server configuration
    use_ssl: bool = True
    enable_docs: bool = False    

    # Logging configuration
    log_level: str = 'INFO'  # Define a default log level

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'allow'  # Allows extra fields

settings = Settings()