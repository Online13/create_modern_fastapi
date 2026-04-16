
type Header = dict[str, str]
class DomainException(Exception):
    code: str | None = None
    headers: Header | None = None
    """Base Exception"""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        headers: Header | None = None,
    ):
        self.message = message
        self.code = code
        self.headers = headers
        super().__init__(self.message)


class NotFoundException(DomainException):
    """Exception raised when a requested resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str | None = None,
        headers: Header | None = None,
    ):
        self.message = message
        self.code = code
        self.headers = headers
        super().__init__(self.message, self.code, self.headers)


class BadRequestException(DomainException):
    """Exception raised when a request is malformed."""

    def __init__(
        self,
        message: str = "Bad request",
        code: str | None = None,
        headers: Header | None = None,
    ):
        self.message = message
        self.code = code
        self.headers = headers
        super().__init__(self.message, self.code, self.headers)


class InternalServerErrorException(DomainException):
    """Exception raised for internal server errors."""

    def __init__(
        self,
        message: str = "Internal server error",
        code: str | None = None,
        headers: Header | None = None,
    ):
        self.message = message
        self.code = code
        self.headers = headers
        super().__init__(self.message, self.code, self.headers)


class ConflictException(DomainException):
    """Exception raised for conflicts, such as duplicate entries."""

    def __init__(
        self,
        message: str = "Conflict",
        code: str | None = None,
        headers: Header | None = None,
    ):
        self.message = message
        self.code = code
        self.headers = headers
        super().__init__(self.message, self.code, self.headers)
