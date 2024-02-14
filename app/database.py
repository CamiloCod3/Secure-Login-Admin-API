from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.schemas.config_schema import settings

# Initialize SSL arguments based on settings
ssl_args = {"ssl": "require"} if settings.use_ssl else {}

# Create the asynchronous engine with possible SSL configuration
async_engine = create_async_engine(
    settings.database_url, 
    echo=False, 
    connect_args=ssl_args
)

# Session factory configured to return asynchronous session instances
AsyncSessionLocal = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Declarative base class for model classes
Base = declarative_base()

async def get_db():
    """Dependency that provides a session for FastAPI route functions."""
    async with AsyncSessionLocal() as db:
        yield db