from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.user_schemas import UserCreateSchema
from ..crud.user_crud import create_user, get_user_by_email
from ..models.user_models import UserModel 
from ..auth.dependencies import is_admin_user 

router = APIRouter()

@router.post("/users/", response_model=UserCreateSchema, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: UserCreateSchema, 
    db: AsyncSession = Depends(get_db), 
    _: UserModel = Depends(is_admin_user)  # Ensure user is admin
):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")    
    user_data = user.model_dump()  
    return await create_user(db=db, user=user_data)