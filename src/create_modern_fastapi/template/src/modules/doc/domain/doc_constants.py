from typing import TypedDict


DOC_TITLE = "Documentation"
DOC_VERSION = "0.1.0"


class SecureDocOption(TypedDict):
    docs_url: str | None
    redoc_url: str | None
    openapi_url: str | None


secure_doc_options: SecureDocOption = {
    "docs_url": None,
    "redoc_url": None,
    "openapi_url": None,
}
