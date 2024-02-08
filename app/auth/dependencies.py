import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError

from ..models.user_models import UserModel
from ..database import get_db
from .oauth2_config import oauth2_scheme
from .jwt_utils import decode_access_token



logger = logging.getLogger(__name__)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession  = Depends(get_db)) -> UserModel:
    """
    Asynchronously authenticates and retrieves the current user from the database.

    Utilizes a JWT token to authenticate the user by decoding it and querying the database for the user details.
    Primarily used as a dependency in secured endpoints to ensure that the requester is authenticated. Raises an
    HTTP 401 Unauthorized exception if the token is invalid, expired, or the user doesn't exist, ensuring secure
    access control.

    Args:
        token (str): JWT token for authentication, extracted from the request headers.
        db (AsyncSession): Async database session for querying user data.

    Returns:
        UserModel: Authenticated user's model instance from the database.

    Raises:
        HTTPException: 401 Unauthorized if authentication fails.
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