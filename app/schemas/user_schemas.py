from pydantic import BaseModel, EmailStr, Field

class BaseUserModel(BaseModel):
    class Config:
        model_config = {
            "from_attributes": True,
            "populate_by_name": True
        }
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
                "name": "John Doe",
                "is_admin": False
            }
        }

class UserCreateSchema(BaseUserModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    name: str
    is_admin: bool = False

class UserCreateResponseSchema(BaseUserModel):
    id: int
    email: EmailStr
    name: str
    is_admin: bool
