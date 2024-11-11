from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import EmailStr, Field, AnyUrl

# Load environment variables from the .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application configuration settings derived from environment variables.
    """
    database_url: AnyUrl
    # Essential JWT settings
    secret_key: str = Field(..., description="Secret key for JWT encoding")
    algorithm: str = "HS256"
    access_token_expires_delta: int = 30
    refresh_token_expires_delta: int = 1440

    # Admin user configuration
    admin_email: EmailStr
    admin_password: str
    admin_name: str = 'Admin'

    # Server configuration
    use_ssl: bool = Field(True, description="Enable SSL for secure connections")
    secure_cookie: bool = Field(True, description="Enable secure cookies")
    enable_docs: bool = False
    log_level: str = 'ERROR'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'allow'

settings = Settings()