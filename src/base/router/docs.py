"""
Module cung cấp redirect từ root path đến Swagger documentation.
"""
from fastapi import APIRouter
from starlette.responses import RedirectResponse


router = APIRouter()


@router.get("/", include_in_schema=False)
async def get_docs() -> RedirectResponse:
    """
    Redirect root path đến Swagger UI.

    Khi truy cập "/" sẽ tự động chuyển hướng đến "/docs"
    để hiển thị API documentation.

    Returns:
        RedirectResponse: Redirect 307 đến /docs.
    """
    return RedirectResponse(url="/docs")
