from decimal import Decimal
from typing import Annotated
from datetime import date

from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator

from app.models.enums import PetSpecies

PetName = Annotated[str, Field(min_length=2, max_length=100)]
PetBreed = Annotated[str, Field(min_length=2, max_length=50)]
PetBirthDate = Annotated[date, Field()]
PetWeight = Annotated[Decimal, Field(gt=0, max_digits=5, decimal_places=2)]

class PetBase(BaseModel):
    name: PetName
    species: PetSpecies
    breed: PetBreed
    birth_date: PetBirthDate
    weight: PetWeight
    
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError('Дата рождения не может быть больше текущей даты')
        return value

class PetCreate(PetBase):
    pass
    
class PetUpdate(BaseModel):
    name: PetName | None = None
    species: PetSpecies | None = None
    breed: PetBreed | None = None
    birth_date: PetBirthDate | None = None
    weight: PetWeight | None = None
    
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, value: date | None) -> date | None:
        if value is not None and value > date.today():
            raise ValueError('Дата рождения не может быть больше текущей даты')
        return value
    
class PetRead(PetBase):
    id: int
    owner_id: int
    
    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        years = today.year - self.birth_date.year
        
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years
    
    model_config = ConfigDict(from_attributes=True)
    
class PetFilter(BaseModel):
    species: PetSpecies | None = None
    breed: str | None = None
    name_contains: str | None = None
    min_weight: PetWeight | None = None
    max_weight: PetWeight | None = None