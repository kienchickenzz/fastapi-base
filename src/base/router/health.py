"""
Module cung cấp health check endpoint.
Endpoint này được sử dụng bởi load balancer và monitoring systems.
"""
from fastapi import APIRouter
from starlette.responses import PlainTextResponse


router = APIRouter()


@router.get("/health", include_in_schema=False, response_class=PlainTextResponse)
async def get_health() -> PlainTextResponse:
    """
    Health check endpoint.

    Trả về "OK" nếu service đang hoạt động bình thường.
    Endpoint này không xuất hiện trong OpenAPI schema.

    Returns:
        PlainTextResponse: "OK" với status 200.
    """
    return PlainTextResponse("OK")
