from enum import Enum

class PetSpecies(str, Enum):
    dog = 'dog'
    cat = 'cat'
    parrot = 'parrot'
    other = 'other'
    
    