from pydantic import BaseModel, EmailStr

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    is_admin: bool = False

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
                "name": "John Doe",
                "is_admin": False
            }
        }