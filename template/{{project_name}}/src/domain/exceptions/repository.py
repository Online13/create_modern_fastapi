class RepositoryIntegrityError(Exception):
    """Custom exception for repository integrity errors."""
    def __init__(self, message: str = "Integrity error"):
        self.message = message
        super().__init__(self.message)

class ResourceNotFoundError(Exception):
    """Custom exception for resource not found errors."""
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)