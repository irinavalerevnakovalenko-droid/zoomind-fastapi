from typing import Annotated

from pydantic import BaseModel,ConfigDict, EmailStr, Field

Username = Annotated[str, Field(min_length=3, max_length=150)]
Password = Annotated[str, Field(min_length=8, max_length=128)]

class UserBase(BaseModel):
    email: EmailStr
    username: Username

class UserCreate(UserBase):
    password: Password
    
class UserLogin(BaseModel):
    login: str
    password: str
    
class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    
    model_config = ConfigDict(from_attributes=True)
    
    
class TokenRead(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    
    
    