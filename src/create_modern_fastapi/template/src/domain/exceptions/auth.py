from .core import DomainException

type Headers = dict[str, str]


class AuthDomainException(DomainException):
    """Base exception for authentication-related errors."""

    def __init__(
        self,
        message: str = "Authentication error occurred.",
        code: str | None = None,
        headers: Headers | None = None,
    ):
        self.message = message
        super().__init__(message, code, headers)


class InvalidCredentialsException(AuthDomainException):
    """Exception raised for invalid user credentials."""

    def __init__(
        self,
        message: str = "Invalid username or password",
        code: str | None = None,
        headers: Headers | None = None,
    ):
        self.message = message
        super().__init__(self.message, code, headers)


class UnauthorizedAccessException(AuthDomainException):
    """Exception raised for unauthorized access attempts."""

    def __init__(
        self,
        message: str = "Unauthorized access",
        code: str | None = None,
        headers: Headers | None = None,
    ):
        self.message = message
        super().__init__(self.message, code, headers)


class TokenExpiredException(AuthDomainException):
    """Exception raised when a token has expired."""

    def __init__(
        self,
        message: str = "Token has expired. Please log in again.",
        code: str | None = None,
        headers: Headers | None = None,
    ):
        super().__init__(message, code, headers)
        self.message = message


class InvalidTokenException(AuthDomainException):
    """Exception raised when a token is invalid."""

    def __init__(
        self,
        message: str = "Invalid token. Please log in again.",
        code: str | None = None,
        headers: Headers | None = None,
    ):
        super().__init__(message, code, headers)
        self.message = message
