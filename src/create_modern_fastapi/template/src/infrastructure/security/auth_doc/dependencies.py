from src.presentation.deps.env import EnvConfig
from src.infrastructure.security.auth_doc.auth_doc_service import AuthDocService


def build_auth_doc_service(env_config: EnvConfig):
    return AuthDocService(
        username=env_config.get_login_docs_username(),
        password=env_config.get_login_docs_password(),
    )
