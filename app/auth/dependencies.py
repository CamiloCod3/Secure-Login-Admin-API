import logging
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError

from ..models.user_models import UserModel
from ..database import get_db
from .jwt_utils import verify_token
from ..schemas.config_schema import settings # Indirect accesed

logger = logging.getLogger(__name__)

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Cookie(None, alias="access_token")) -> UserModel:
    """
    Retrieves the authenticated user based on a JWT token from cookies.

    Args:
        db: Database session for user data querying.
        token: JWT token for authentication.

    Returns:
        The authenticated UserModel instance or raises HTTPException for errors.
    """

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = verify_token(token, credentials_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ))
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid JWT token")
        user_query = select(UserModel).filter(UserModel.email == email)
        user = await db.execute(user_query)
        user = user.scalars().first()
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")



async def is_admin_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """
    Verifies if the authenticated user has admin privileges.

    Args:
        current_user: The authenticated UserModel instance.

    Returns:
        The UserModel if admin, otherwise raises HTTPException for insufficient privileges.
    """
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user