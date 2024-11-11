from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from ..database import get_db
from ..auth.dependencies import get_current_user, is_admin_user
from ..models.user_models import UserModel
from ..schemas.user_schemas import UserCreateSchema, UserCreateResponseSchema
from ..crud.user_crud import get_user_by_email, create_user
from ..utils.rate_limiter import limiter  # Import the rate limiter

router = APIRouter()

@router.post("/users/", response_model=UserCreateResponseSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # Set rate limit
async def create_user_endpoint(
    request: Request,  # Added request argument for rate limiting
    response: Response,
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
    _current_authenticated_user: UserModel = Depends(get_current_user),
    _current_user: UserModel = Depends(is_admin_user)
) -> Any:
    """
    Creates a new user in the system with specified details.
    """
    # Check if email is already registered
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user using CRUD function
    new_user = await create_user(db, user.model_dump())

    # Return formatted response
    return UserCreateResponseSchema.model_validate(new_user, from_attributes=True)
