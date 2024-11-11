from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Response
from ..schemas.config_schema import settings

class JWTTokenHandler:

    @staticmethod
    def create_access_token(*, data: dict, expires_delta: int = None):
        """Create a JWT access token with an expiration time."""
        expires_in_minutes = expires_delta if expires_delta is not None else settings.access_token_expires_delta
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)  # Timezone-aware datetime
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(*, data: dict, expires_delta: int = None):
        """Create a JWT refresh token with an expiration time."""
        expires_in_minutes = expires_delta if expires_delta is not None else settings.refresh_token_expires_delta
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)  # Timezone-aware datetime
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, credentials_exception, is_refresh_token=False):
        """Verify the JWT token and ensure required claims are present."""
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm],
                options={"verify_signature": True, "verify_exp": True}  # Enforce signature and expiration verification
            )
            # Ensure the token contains the expected 'sub' claim and, for refresh tokens, the 'refresh' claim
            if 'sub' not in payload or (is_refresh_token and 'refresh' not in payload):
                raise credentials_exception
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise credentials_exception

    @staticmethod
    def decode_access_token(token: str):
        """Decode the access token, raising an exception if expired or invalid."""
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm],
                options={"verify_signature": True, "verify_exp": True}  # Enforce verification
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def set_refresh_token_cookie(response: Response, refresh_token: str):
        """Set the refresh token in a secure, HTTP-only cookie."""
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.secure_cookie,
            samesite="Lax"
        )

    @staticmethod
    def clear_refresh_token_cookie(response: Response):
        """Clear the refresh token from the cookies."""
        response.delete_cookie("refresh_token", httponly=True, secure=settings.secure_cookie, samesite='Lax', path='/')

    @staticmethod
    def clear_access_token_cookie(response: Response):
        """Clear the access token from the cookies."""
        response.delete_cookie("access_token", httponly=True, secure=settings.secure_cookie, samesite='Lax', path='/')
