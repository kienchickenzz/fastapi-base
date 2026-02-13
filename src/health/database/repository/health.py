"""
Repository cho HealthCheck entity.
Cung cấp các operations đặc thù cho health check data.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.health.database.model.health_check import HealthCheck


class HealthCheckRepository(Repository[HealthCheck]):
    """
    Repository để quản lý HealthCheck entities.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine
    """

    def __init__(self, engine: AsyncEngine):
        super().__init__(engine, HealthCheck)


    async def get_latest_check(self) -> Optional[HealthCheck]:
        """
        Lấy health check mới nhất từ database.

        Returns:
            Optional[HealthCheck]: HealthCheck entity hoặc None nếu không có
        """
        query = """
            SELECT *
            FROM health_check
            ORDER BY created_at DESC
            LIMIT 1
        """
        results = await self.fetch_sql(query)

        if not results:
            return None

        return HealthCheck(**dict(results[0]))
    