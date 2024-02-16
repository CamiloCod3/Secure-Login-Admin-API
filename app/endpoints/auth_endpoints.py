import logging
from fastapi import APIRouter, HTTPException, status, Request, Response, Cookie, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from ..database import get_db
from ..auth import password_utils
from ..auth.jwt_utils import JWTTokenHandler
from ..auth.oauth2_config import OAuth2PasswordBearerWithCookie
from ..crud.user_crud import get_user_by_email
from ..utils.rate_limiter import limiter
from ..schemas.config_schema import settings

logger = logging.getLogger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")

@router.post("/token")
@limiter.limit("5/minute")
async def login(
    request: Request,  # Include Request for SlowAPI
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
    """
    
    user = await get_user_by_email(db, form_data.username)
    
    if not user or not password_utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    
    # Generate JWT tokens
    access_token = JWTTokenHandler.create_access_token(data={"sub": user.email})
    refresh_token = JWTTokenHandler.create_refresh_token(data={"sub": user.email})

    # Set the refresh token in an HTTP-only cookie
    JWTTokenHandler.set_refresh_token_cookie(response, refresh_token)
    # Additionally, set the access token in an HTTP-only cookie for enhanced security
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.secure_cookie,  # Secure by default, overridden in local dev as needed
        samesite='Lax'  # Helps prevent CSRF attacks
    )  

    return {
    "message": "Login successful",
    "is_admin": user.is_admin  
}


@router.post("/refresh_token")
async def refresh_token(
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: str = Cookie(None, alias="refresh_token")  # Extract refresh token from cookies
):
    """
    Refreshes an access token using a valid refresh token provided as an HTTP-only cookie.

    This endpoint checks for a valid refresh token and, if found, issues a new access token.
    The new access token is then sent back to the client as an HTTP-only cookie, ensuring
    the continuation of the authenticated session. If the refresh token is missing, invalid,
    or expired, an error is returned.

    Args:
        response: Response object for setting cookies.
        db: Database session for potential user verification (not utilized here).
        refresh_token: Refresh token extracted from cookies.

    Returns:
        A success message indicating the access token has been refreshed.
    """

    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        # Verify the refresh token and get a new access token
        user_email = JWTTokenHandler.verify_token(refresh_token, credentials_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        ))["sub"]
        new_access_token = JWTTokenHandler.create_access_token(data={"sub": user_email})        
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
    This endpoint clears the HTTP-only access and refresh token cookies from the client.
    """
    # Clears the refresh token cookie using JWTTokenHandler
    JWTTokenHandler.clear_refresh_token_cookie(response)
    # Clears the access token cookie using JWTTokenHandler
    JWTTokenHandler.clear_access_token_cookie(response)
    
    return {"message": "Logged out successfully"}