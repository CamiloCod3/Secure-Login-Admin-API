import logging
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from ..database import get_db
from ..auth import jwt_utils, password_utils
from ..auth.oauth2_config import oauth2_scheme
from ..crud.auth_crud import get_user_by_email


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/token")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)    
):
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

    # Set access and refresh tokens using jwt_utils
    jwt_utils.set_refresh_token_cookie(response, refresh_token)  # Sets the refresh token in an HTTP-only cookie
    # Include access_token in the response body or set it in another way if required
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh_token")
async def refresh_token(
    response: Response,
    current_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)    
):
    try:
        # Verify the current token and get a new access token
        user_email = jwt_utils.verify_token(current_token, credentials_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        ))["sub"]
        new_access_token = jwt_utils.create_access_token(data={"sub": user_email})
        # Refresh the refresh token
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.post("/logout")
async def logout(response: Response):
    jwt_utils.clear_refresh_token_cookie(response)  # Clears the refresh token cookie
    return {"message": "Logged out successfully"}