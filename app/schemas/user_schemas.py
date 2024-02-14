from pydantic import BaseModel, EmailStr

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
    password: str
    name: str
    is_admin: bool = False

class UserCreateResponseSchema(BaseUserModel):
    id: int
    email: EmailStr
    name: str
    is_admin: bool