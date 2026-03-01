
class NotFoundException(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)

class BadRequestException(Exception):
    def __init__(self, message: str = "Bad request"):
        self.message = message
        super().__init__(self.message)

class InternalServerErrorException(Exception):
    def __init__(self, message: str = "Internal server error"):
        self.message = message
        super().__init__(self.message)

class ConflictException(Exception):
    def __init__(self, message: str = "Conflict"):
        self.message = message
        super().__init__(self.message)