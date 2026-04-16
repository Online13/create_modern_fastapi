from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.domain.exceptions.auth import InvalidCredentialsException
from src.domain.interfaces.services.auth_doc_service import AuthDocService
from src.infrastructure.security.auth_doc.dependencies import build_auth_doc_service

security = HTTPBasic()


def auth_doc(
    auth_doc_service: AuthDocService = Depends(build_auth_doc_service),
    credentials: HTTPBasicCredentials = Depends(security),
):
    is_valid = auth_doc_service.validate(
        username=credentials.username, password=credentials.password
    )

    if not is_valid:
        raise InvalidCredentialsException(
            message="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
