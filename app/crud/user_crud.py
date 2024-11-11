import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..auth.password_utils import hash_password
from ..utils.error_handlers import exception_handler
from ..models.user_models import UserModel

# Configure logging
logger = logging.getLogger(__name__)

@exception_handler
async def get_user_by_email(db: AsyncSession, email: str):
    """Retrieve a user by email."""
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if user:
        logger.info(f"User with email {email} retrieved successfully.")
    else:
        logger.warning(f"User with email {email} not found.")
    return user

@exception_handler
async def create_user(db: AsyncSession, user: dict) -> UserModel:
    """Create new user."""
    hashed_password = hash_password(user['password'])
    db_user = UserModel(
        email=user['email'],
        password_hash=hashed_password,
        name=user['name'],
        is_admin=user['is_admin']
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    logger.info(f"Created new user with email: {user['email']}")
    return db_user