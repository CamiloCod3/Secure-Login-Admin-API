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
    Asynchronously retrieves the current user based on a provided JWT token.

    This function decodes the JWT token to extract user information and queries the database to retrieve the user model.
    If the user is not found, or if the token is invalid or expired, an HTTP 401 Unauthorized exception is raised.

    Args:
    - token (str): A JWT token used for user authentication. Default dependency is `oauth2_scheme`.
    - db (AsyncSession): An asynchronous session to the database. Default dependency is `get_db`.

    Returns:
    - UserModel: The user model of the authenticated user.

    Raises:
    - HTTPException: With a 401 status code if the user cannot be authenticated or if any other exception occurs during the process.
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