class SubSonicException(Exception):
    """Base exception for SubSonic Festival"""
    pass

class NotFoundException(SubSonicException):
    """Resource not found"""
    pass

class ValidationException(SubSonicException):
    """Validation error"""
    pass

class DatabaseException(SubSonicException):
    """Database operation error"""
    pass

class UnauthorizedException(SubSonicException):
    """User not authorized"""
    pass

class ConflictException(SubSonicException):
    """Resource conflict (e.g., duplicate user email)"""
    pass
