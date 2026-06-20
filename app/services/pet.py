from app.core.exceptions import PetNotFoundError
from app.repositories.pet import AbstractPetRepository
from app.schemas.pet import PetCreate, PetUpdate
from app.models.pet import Pet

class PetService:
    def __init__(self, repository: AbstractPetRepository):
        self.repository = repository
        
    async def create_pet(self, owner_id: int, pet_data: PetCreate) -> Pet:
        pet = await self.repository.create(
            owner_id=owner_id,
            name=pet_data.name,
            species=pet_data.species,
            breed=pet_data.breed,
            age=pet_data.age,
            weight=pet_data.weight,   
        )
        
        return pet
    
    async def list_pets(self, owner_id: int) -> list[Pet]:
        return await self.repository.list_for_owner(owner_id)
    
    async def get_pet(self, pet_id: int, owner_id: int) -> Pet:
        pet = await self.repository.get_by_id(pet_id, owner_id)
        
        if pet is None:
            raise PetNotFoundError()
        
        return pet
    
    async def update_pet(
        self, 
        pet_id: int,
        owner_id: int, 
        pet_data: PetUpdate,
        ) -> Pet:
        pet = await self.get_pet(pet_id, owner_id)
        data = pet_data.model_dump(exclude_unset=True)
        return await self.repository.update(pet, data)
    
    async def delete_pet(self, pet_id: int, owner_id: int) -> None:
        pet = await self.get_pet(pet_id, owner_id)
        await self.repository.delete(pet)
        