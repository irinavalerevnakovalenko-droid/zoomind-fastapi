from enum import Enum

class PetSpecies(str, Enum):
    dog = 'dog'
    cat = 'cat'
    parrot = 'parrot'
    other = 'other'
    
class ProductCategory(str, Enum):
    food = 'food'
    toy = 'toy'
    accessory = 'accessory'
    medicine = 'medicine'
    other = 'other'
    
class ProductSpecies(str, Enum):
    dog = 'dog'
    cat = 'cat'
    parrot = 'parrot'
    universal = 'universal'
    other = 'other'
    
    