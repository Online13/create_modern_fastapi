from typing import Protocol


class AuthDocService(Protocol):

    def validate(self, username: str, password: str) -> bool: ...
