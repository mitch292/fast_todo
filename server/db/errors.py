class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""

class EntityAlreadyExists(Exception):
    """Raised when entity exists already in the database."""