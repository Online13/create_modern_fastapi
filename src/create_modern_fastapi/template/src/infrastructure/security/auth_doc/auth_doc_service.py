import secrets


class AuthDocService:

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def validate(self, username: str, password: str) -> bool:
        correct_username = secrets.compare_digest(username, self.username)
        correct_password = secrets.compare_digest(password, self.password)

        return correct_username and correct_password
