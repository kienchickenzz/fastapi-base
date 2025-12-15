from src.health.database.model.health_check.main import HealthCheck
from src.health.database.repository.base.main import BaseRepository

import logging
logger = logging.getLogger(__name__)

class HealthCheckRepository(BaseRepository[HealthCheck]):
    
    def __init__(self, engine):
        super().__init__(engine, HealthCheck)


    async def get_latest_check(self) -> HealthCheck:
        """
        Fetch the latest health check entry from the database.

        :return: The latest HealthCheck entity (row)
        :rtype: HealthCheck
        """
        parsed_result: HealthCheck
        async with self._get_session() as session:
            query = """
                SELECT *
                FROM health_check
                ORDER BY created_at DESC
                LIMIT 1
            """
            results = await self.execute_sql(query)
            if isinstance(results, int):
                raise RuntimeError(f"Expected SELECT query results, got integer: {results}")
            parsed_result = HealthCheck(**dict(results[0]))

        if not results:
            raise RuntimeError("No health check records found.")

        return parsed_result
    