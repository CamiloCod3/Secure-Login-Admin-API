import logging
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from ..database import get_db
from ..auth import jwt_utils, password_utils
from ..auth.oauth2_config import oauth2_scheme
from ..crud.user_crud import get_user_by_email
from ..utils.rate_limiter import limiter
from ..schemas.config_schema import settings

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/token")
@limiter.limit("5/minute")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)    
):
    """
    Authenticate a user and return JWT access and refresh tokens.

    This endpoint verifies user credentials and, if valid, returns a set of JWT tokens.
    The access token is returned as part of the response body, and the refresh token
    is set as an HTTP-only cookie for enhanced security. Rate-limited to prevent abuse.

    Args:
        response: FastAPI response object, used to set the refresh token cookie.
        form_data: OAuth2PasswordRequestForm containing the username (email) and password.
        db: Database session dependency injection to access user data.
    
    Raises:
        HTTPException: 401 error if authentication fails due to incorrect credentials.    
    """

    user = await get_user_by_email(db, form_data.username)
    if not user or not password_utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    # Generate JWT tokens
    access_token = jwt_utils.create_access_token(data={"sub": user.email})
    refresh_token = jwt_utils.create_refresh_token(data={"sub": user.email})

    # Set the refresh token in an HTTP-only cookie
    jwt_utils.set_refresh_token_cookie(response, refresh_token)
    # Additionally, set the access token in an HTTP-only cookie for enhanced security
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.secure_cookie,  # Secure by default, overridden in local dev as needed
        samesite='Lax'  # Helps prevent CSRF attacks
    )  

    return {"message": "Login successful"}


@router.post("/refresh_token")
async def refresh_token(
    response: Response,
    current_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)    
):
    """
    Refresh JWT access tokens using a valid refresh token.

    This endpoint validates the provided refresh token and issues a new access token if the
    refresh token is valid. The new access token is returned as an HTTP-only cookie.

    Args:
        response: FastAPI response object, used to set the new access token cookie.
        current_token: The refresh token extracted from the request's cookies.
        db: Database session dependency injection for potential user verification.
    
    Raises:
        HTTPException: 401 error if the refresh token is invalid or expired.    
    Returns:
        A success message indicating the access token has been refreshed.
    """
    try:
        # Verify the current token and get a new access token
        user_email = jwt_utils.verify_token(current_token, credentials_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        ))["sub"]
        new_access_token = jwt_utils.create_access_token(data={"sub": user_email})        
        # Set the new access token in an HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=settings.secure_cookie,  # Secure by default, overridden in local dev as needed
            samesite='Lax'  # Helps prevent CSRF attacks
        )
                
        return {"message": "Access token refreshed successfully"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/logout")
async def logout(response: Response):
    """
    Log out a user by clearing the refresh token cookie.

    This endpoint clears the HTTP-only refresh token cookie from the client, effectively
    logging the user out. Consider adding server-side token invalidation.
    """
    jwt_utils.clear_refresh_token_cookie(response)  # Clears the refresh token cookie
    return {"message": "Logged out successfully"}