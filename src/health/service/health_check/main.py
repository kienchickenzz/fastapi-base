"""
Health check service module.
Chứa business logic cho các operations liên quan đến health check.
"""

import logging

from src.health.database.repository.health import HealthCheckRepository
from src.health.dto.main import (
    DbHealthCheckDto,
    DbHealthCheckResponseDto,
    DbHealthCheckCreateResponse,
)


logger = logging.getLogger("app")


class HealthCheckService:
    """
    Service xử lý các operations liên quan đến health check.

    Args:
        health_check_repository (HealthCheckRepository): Repository để truy cập database
    """

    def __init__(self, health_check_repository: HealthCheckRepository):
        self._repository = health_check_repository

    async def check_db_health(self) -> DbHealthCheckCreateResponse:
        """
        Tạo một health check entry mới để verify database connection.

        Returns:
            DbHealthCheckCreateResponse: Response chứa message và id của entry vừa tạo
        """
        entity = await self._repository.create({})
        logger.info(f"Created health check entry with id={entity.id}")
        return DbHealthCheckCreateResponse(message="DB OK", id=entity.id)

    async def get_db_health_checks(
        self,
        target_page: int,
        page_size: int,
    ) -> DbHealthCheckResponseDto:
        """
        Lấy danh sách health check entries với pagination.

        Args:
            target_page (int): Trang cần lấy (1-indexed)
            page_size (int): Số records mỗi trang

        Returns:
            DbHealthCheckResponseDto: Response chứa danh sách health checks và pagination info
        """
        skip = (target_page - 1) * page_size
        result, count = await self._repository.get_multiple(
            limit=page_size,
            skip=skip,
        )

        total_pages = (count + page_size - 1) // page_size
        return DbHealthCheckResponseDto(
            health_checks=[DbHealthCheckDto.model_validate(item) for item in result],
            current_page=target_page,
            total_pages=total_pages,
            page_size=page_size,
        )

    async def get_latest_db_health_check(self) -> DbHealthCheckDto:
        """
        Lấy health check entry mới nhất.

        Returns:
            DbHealthCheckDto: Health check entry mới nhất

        Raises:
            ValueError: Nếu không có health check nào trong database
        """
        result = await self._repository.get_latest_check()
        if result is None:
            raise ValueError("No health check records found")
        return DbHealthCheckDto.model_validate(result)
