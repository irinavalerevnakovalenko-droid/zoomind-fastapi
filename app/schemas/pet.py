from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import PetSpecies

PetName = Annotated[str, Field(min_length=2, max_length=100)]
PetBreed = Annotated[str, Field(min_length=2, max_length=50)]
PetAge = Annotated[int, Field(ge=0, le=100)]
PetWeight = Annotated[Decimal, Field(gt=0, max_digits=5, decimal_places=2)]

class PetBase(BaseModel):
    name: PetName
    species: PetSpecies
    breed: PetBreed
    age: PetAge
    weight: PetWeight

class PetCreate(PetBase):
    pass
    
class PetUpdate(BaseModel):
    name: PetName | None = None
    species: PetSpecies | None = None
    breed: PetBreed | None = None
    age: PetAge | None = None
    weight: PetWeight | None = None
    
class PetRead(PetBase):
    id: int
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class PetFilter(BaseModel):
    species: PetSpecies | None = None
    breed: str | None = None
    name_contains: str | None = None
    min_weight: PetWeight | None = None
    max_weight: PetWeight | None = None