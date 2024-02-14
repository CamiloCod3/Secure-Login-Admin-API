from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from ..database import get_db
from ..auth.dependencies import get_current_user, is_admin_user
from ..models.user_models import UserModel
from ..schemas.user_schemas import UserCreateSchema, UserCreateResponseSchema
from ..crud.user_crud import get_user_by_email, create_user

router = APIRouter()

@router.post("/users/", response_model=UserCreateResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    response: Response,
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
    _current_authenticated_user: UserModel = Depends(get_current_user),  # Authenticate the user
    _current_user: UserModel = Depends(is_admin_user)  # Authorize admin-only access
) -> Any:
    """
    Creates a new user in the system with specified details.

    This endpoint is protected and requires admin privileges. It validates the provided user details against the UserCreateSchema,
    checks if the email is not already registered, hashes the password, and stores the new user in the database.
    Finally, it returns the created user details excluding the password hash.

    Parameters:
    - response (Response): The response object used to set cookies or modify the HTTP response.
    - user (UserCreateSchema): The user details from the request body. Expected schema includes email, password, name, and is_admin flag.
    - db (AsyncSession): Dependency injection of the database session for executing database operations.
    - _current_authenticated_user (UserModel): The current authenticated user performing the request, injected automatically.
    - _current_user (UserModel): Ensures that the endpoint is accessed by an admin user, injected automatically.

    Returns:
    - UserCreateResponseSchema: The created user's details, including id, email, name, and is_admin flag. 

    The function uses SQLAlchemy for database interactions and Pydantic for request and response serialization.
    """
    # Check if email is already registered
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Use CRUD function to create new user
    new_user = await create_user(db, user.model_dump())

    # Create a Pydantic model instance from the ORM model
    response_model = UserCreateResponseSchema.model_validate(new_user, from_attributes=True)
    return response_model