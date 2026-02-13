"""
DTOs cho health check module.
Định nghĩa các request/response models cho health check endpoints.
"""

from datetime import datetime

from pydantic import field_serializer

from src.base.dto.main import PaginatedRequestBase, PaginatedResponseBase, ResponseBase


class DbHealthCheckRequest(PaginatedRequestBase):
    """
    Request params cho endpoint lấy danh sách health checks.
    """

    pass


class DbHealthCheckDto(ResponseBase):
    """
    DTO đại diện cho một health check entry.

    Attributes:
        id (int): ID của health check
        created_at (datetime): Thời điểm tạo
        updated_at (datetime): Thời điểm cập nhật
    """

    id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, value: datetime) -> str:
        """
        Serialize datetime thành ISO format string.

        Args:
            value (datetime): Giá trị datetime

        Returns:
            str: ISO format string
        """
        return value.isoformat() if value else None  # type: ignore


class DbHealthCheckCreateResponse(ResponseBase):
    """
    Response khi tạo health check thành công.

    Attributes:
        message (str): Thông báo kết quả
        id (int): ID của health check vừa tạo
    """

    message: str
    id: int


class DbHealthCheckResponseDto(PaginatedResponseBase):
    """
    Response chứa danh sách health checks với pagination.

    Attributes:
        health_checks (list[DbHealthCheckDto]): Danh sách health checks
    """

    health_checks: list[DbHealthCheckDto]
