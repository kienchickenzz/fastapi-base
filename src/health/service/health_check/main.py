from src.health.database.repository.health_check.main import HealthCheckRepository
from src.health.dto.main import (
    DbHealthCheckDto, DbHealthCheckResponseDto
)

import logging
logger = logging.getLogger(__name__)

class HealthCheckService:
    def __init__(self, health_check_repository: HealthCheckRepository):
        self.health_check_repository = health_check_repository

    async def check_health(self) -> None:
        await self.health_check_repository.create({})

    async def check_db_health(self) -> None:
        await self.health_check_repository.create({})

    async def get_db_health_checks(self, target_page: int, page_size: int):
        skip = (target_page - 1) * page_size
        result, count = await self.health_check_repository.get_multiple(
            limit=page_size,
            skip=skip,
        )

        total_pages = (count + page_size - 1) // page_size
        return DbHealthCheckResponseDto(
            health_checks=[ DbHealthCheckDto( **item.__dict__ ) for item in result ],
            current_page=target_page,
            total_pages=total_pages,
            page_size=page_size,
        )

    async def get_latest_db_health_check(self) -> DbHealthCheckDto:
        result = await self.health_check_repository.get_latest_check()
        logger.info(result)
        return DbHealthCheckDto(**result.__dict__)
