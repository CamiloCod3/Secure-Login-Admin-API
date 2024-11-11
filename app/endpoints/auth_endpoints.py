import logging
from fastapi import APIRouter, HTTPException, status, Request, Response, Cookie, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt.exceptions import PyJWTError

from ..database import get_db
from ..auth import password_utils
from ..auth.jwt_utils import JWTTokenHandler
from ..auth.oauth2_config import OAuth2PasswordBearerWithCookie
from ..crud.user_crud import get_user_by_email
from ..utils.rate_limiter import limiter
from ..schemas.config_schema import settings

logger = logging.getLogger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.post("/token")
@limiter.limit("5/minute")
async def login(
    request: Request,  # Required for rate limiting
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Authenticate a user and return JWT access and refresh tokens."""
    
    user = await get_user_by_email(db, form_data.username)
    
    if not user or not password_utils.verify_password(form_data.password, user.password_hash):
        logger.warning(f"Failed login attempt for email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = JWTTokenHandler.create_access_token(data={"sub": user.email})
    refresh_token = JWTTokenHandler.create_refresh_token(data={"sub": user.email})

    JWTTokenHandler.set_refresh_token_cookie(response, refresh_token)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.secure_cookie,
        samesite='Lax'
    )

    logger.info(f"User {form_data.username} logged in successfully.")
    return {"message": "Login successful", "is_admin": user.is_admin}

@router.post("/refresh_token")
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: str = Cookie(None, alias="refresh_token")
):
    """Refreshes an access token using a valid refresh token provided as an HTTP-only cookie."""

    if refresh_token is None:
        logger.warning("Attempt to refresh token without a refresh token cookie.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        user_email = JWTTokenHandler.verify_token(refresh_token, credentials_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ))["sub"]

        new_access_token = JWTTokenHandler.create_access_token(data={"sub": user_email})
        
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=settings.secure_cookie,
            samesite='Lax'
        )

        logger.info(f"Access token refreshed successfully for user {user_email}.")
        return {"message": "Access token refreshed successfully"}
    
    except PyJWTError:
        logger.error("Invalid refresh token attempt.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.post("/logout")
@limiter.limit("5/minute")
async def logout(request: Request, response: Response):
    """Clear the HTTP-only access and refresh token cookies from the client."""
    JWTTokenHandler.clear_refresh_token_cookie(response)
    JWTTokenHandler.clear_access_token_cookie(response)
    logger.info("User logged out successfully.")
    
    return {"message": "Logged out successfully"}
