from fastapi import APIRouter, HTTPException, status, Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.user_schemas import UserCreateSchema
from ..crud.user_crud import create_user, get_user_by_email
from ..models.user_models import UserModel
from ..auth.dependencies import get_current_user, is_admin_user
from ..schemas.config_schema import settings

router = APIRouter()

@router.post("/users/", response_model=UserCreateSchema, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    response: Response,
    user: UserCreateSchema, 
    db: AsyncSession = Depends(get_db),
    # This line ensures we are ready to receive the token from cookies.
    # The actual extraction and validation happen in the get_current_user dependency.
    current_user: UserModel = Depends(get_current_user)):
    # The admin check is performed on the current_user obtained from the dependency.
    # This means the token has already been validated, and the user's admin status has been verified.
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Creating a new user
    user_data = user.model_dump()  # Ensure you are using .dict() method correctly as per Pydantic version
    created_user = await create_user(db=db, user=user_data)
    
    # Optionally, set a new token or update response if needed
    # For example, you could return a confirmation message or the created user data
    
    return created_user