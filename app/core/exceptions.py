class AppError(Exception):
    pass

class EmailAlreadyExistsError(AppError):
    pass

class UsernameAlreadyExistsError(AppError):
    pass

class InvalidCredentialsError(AppError):
    pass

class PetNotFoundError(AppError):
    pass

class InvalidTokenError(AppError):
    pass

