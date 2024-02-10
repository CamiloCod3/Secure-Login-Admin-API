import logging
from fastapi import Depends, HTTPException, Cookie, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError

from ..models.user_models import UserModel
from ..database import get_db
from .oauth2_config import oauth2_scheme
from .jwt_utils import decode_access_token



logger = logging.getLogger(__name__)


async def get_current_user(token: str = Cookie(None), db: AsyncSession = Depends(get_db)) -> UserModel:
    """
    Authenticates and retrieves the current user based on a provided JWT token.

    This function decodes the JWT token to extract user information and retrieves the user's details from the database.
    It's used to authenticate requests in secured endpoints. If the token is invalid, expired, or if the user does not exist,
    an HTTP 401 Unauthorized exception is raised.

    Args:
        token (str): JWT token for authentication, typically extracted from cookies or authorization headers.
        db (AsyncSession): Database session for user data retrieval.

    Returns:
        UserModel: The authenticated user's database model instance.

    Raises:
        HTTPException: 401 Unauthorized if token validation fails.
"""    

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        result = await db.execute(select(UserModel).filter(UserModel.email == payload.get("sub")))
        user = result.scalars().first()
        
        if user is None:
            raise credentials_exception

        return user

    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise credentials_exception

    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        raise credentials_exception
    

async def is_admin_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """
    Verifies that the current authenticated user is an admin.

    This function is intended to be used as a dependency in FastAPI endpoints that require the user
    to have admin privileges. It raises an HTTP 403 Forbidden exception if the current user is not an admin.

    Args:
        current_user (UserModel): The user model instance of the currently authenticated user, 
                                  obtained from `get_current_user`.

    Returns:
        UserModel: The model instance of the admin user if the check passes.

    Raises:
        HTTPException: 403 Forbidden if the current user is not an admin.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user