from typing import Annotated

from pydantic import BaseModel,ConfigDict, EmailStr, Field, model_validator

Username = Annotated[str, Field(min_length=3, max_length=150)]
Password = Annotated[str, Field(min_length=8, max_length=128)]
Phone = Annotated[str, Field(min_length=3, max_length=30)]
DeliveryAddress = Annotated[str, Field(max_length=255)]

class UserBase(BaseModel):
    email: EmailStr
    username: Username
    phone: Phone
    delivery_address: DeliveryAddress = ''
    is_newsletter_enabled: bool = False

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
    
class UserUpdate(BaseModel):
    phone: Phone | None = None
    delivery_address: DeliveryAddress | None = None
    is_newsletter_enabled: bool | None = None
    
    @model_validator(mode='after')
    def validate_phone(self) -> 'UserUpdate':
        if 'phone' in self.model_fields_set and self.phone is None:
            raise ValueError('Поле обязательно для заполнения')
        return self
    
    
class TokenRead(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    
    
    
