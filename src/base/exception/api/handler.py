"""
Exception handlers cho FastAPI application.
Xử lý các loại exception và convert thành HTTP response phù hợp.
"""

import traceback
from http import HTTPStatus
from typing import Any, Type, Union

from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from src.base.exception.api.base import HTTPException


async def rest_exception_handler(_: Request, exc: HTTPException) -> Response:
    """
    Handle HTTPException (business logic errors).

    Args:
        _ (Request): Request object (unused)
        exc (HTTPException): HTTPException instance

    Returns:
        Response: JSONResponse with proper status code and payload
    """
    return exc.get_body()


async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
    """
    Handle ValueError (invalid input).

    Args:
        _ (Request): Request object (unused)
        exc (ValueError): ValueError instance

    Returns:
        JSONResponse: Response with 400 Bad Request
    """
    traceback.print_exception(type(exc), exc, exc.__traceback__)
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST.value,
        content={"detail": str(exc) or HTTPStatus.BAD_REQUEST.phrase},
    )


async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unhandled exceptions.

    Args:
        _ (Request): Request object (unused)
        exc (Exception): Any unhandled exception

    Returns:
        JSONResponse: Response with 500 Internal Server Error
    """
    traceback.print_exception(type(exc), exc, exc.__traceback__)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content={"detail": HTTPStatus.INTERNAL_SERVER_ERROR.phrase},
    )


def compose_exceptions(*exceptions: Type[HTTPException]) -> dict[Union[int, str], dict[str, Any]]:
    """
    Compose exceptions for OpenAPI documentation.

    Args:
        *exceptions (Type[HTTPException]): HTTPException subclasses to document

    Returns:
        dict: OpenAPI responses schema
    """
    responses: dict = {}

    for exception in exceptions:
        responses.update(exception.get_description())

    return responses
