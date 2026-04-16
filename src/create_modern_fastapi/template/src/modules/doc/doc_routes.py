from fastapi import APIRouter, Depends, Request
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from src.modules.doc.doc_deps import auth_doc
from src.modules.doc.domain.doc_constants import DOC_TITLE, DOC_VERSION


router = APIRouter()


@router.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def get_docs(_: str = Depends(auth_doc)) -> HTMLResponse:
    print('Accessing /docs endpoint')
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="docs",
        swagger_ui_parameters={"defaultModelsExpandDepth": 0},
    )

@router.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
async def get_redoc(_: str = Depends(auth_doc)) -> HTMLResponse:
    return get_redoc_html(openapi_url="/api/openapi.json", title="redoc")


@router.get("/api/openapi.json", include_in_schema=False)
async def openapi(request: Request, _: str = Depends(auth_doc)):
    return get_openapi(version=DOC_VERSION, title=DOC_TITLE, routes=request.app.routes)
