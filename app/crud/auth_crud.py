import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..utils.error_handlers import exception_handler
from ..models.user_models import UserModel

# Configure logging
logger = logging.getLogger(__name__)


@exception_handler
async def get_user_by_email(db: AsyncSession, email: str):
    """Retrieve a user by email."""
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    return result.scalar_one_or_none()
