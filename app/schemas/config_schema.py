from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    """
Application configuration settings derived from environment variables.

Attributes:
    Essential JWT settings:
        secret_key (str): Secret key used for JWT encoding and decoding.
        algorithm (str): Algorithm used for JWT operations, default is "HS256".
        access_token_expires_delta (int): Expiration time for access tokens in minutes, default is 30 minutes.
        refresh_token_expires_delta (int): Expiration time for refresh tokens in minutes, default is 1440 minutes (24 hours).

    Admin user configuration:
        admin_email (EmailStr): Email address for the initial admin user.
        admin_password (str): Password for the initial admin user.
        admin_name (str): Name for the initial admin user, default is "Admin".

    Server configuration:
        use_ssl (bool): Flag to indicate if SSL should be used, default is True for secure connections. Override in development environment if necessary.
        enable_docs (bool): Flag to enable or disable FastAPI documentation routes (Swagger UI and ReDoc), default is False to enhance security.
        log_level (str): Default logging level, default is "INFO". Recommended to set to "WARNING" or higher in production environments.
        secure_cookie (bool): Flag to indicate if cookies should be marked as secure, meaning they are only sent over HTTPS.
        Default is True, ensuring cookies are transmitted securely. Override to False in local development environments without HTTPS.
    """
    # Essential JWT settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expires_delta: int = 30  # Expires in 30 minutes
    refresh_token_expires_delta: int = 1440  # Expires in 24 hours (1440 minutes)

    # Admin user configuration
    admin_email: EmailStr
    admin_password: str
    admin_name: str = 'Admin' 

    # Server configuration    
    use_ssl: bool = True
    secure_cookie: bool = True # Toggle for secure cookies, defaulting to True for security
    enable_docs: bool = False      
    log_level: str = 'ERROR'

    class Config:
        """
        Configuration class to specify the source of environment variables.
        
        Attributes:
            env_file (str): Path to the .env file from which to load environment variables.
            env_file_encoding (str): Encoding of the .env file.
            extra (str): Policy for handling extra attributes during model initialization.
        """

        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'allow'  # Allows extra fields

settings = Settings()