from types import TracebackType
from typing import Optional, Type

from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import FastAPI

from src.base.initializer import State, Initializer
from src.health.database.repository.health import HealthCheckRepository
from src.health.service.health_check.main import HealthCheckService

class ServiceState(State):
    # Services
    health_check_service: HealthCheckService
    # Repositories
    db_engine: AsyncEngine
    health_check_repository: HealthCheckRepository

class HealthInitializer(Initializer):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app=app)

    async def __aenter__(self) -> ServiceState:
        state = await super().__aenter__()

        # DB engine
        db_engine = self.engine_factory.create_engine("DB")

        # Initialize utilities

        # Initialize repositories
        health_check_repository = HealthCheckRepository(engine=db_engine)

        # Initialize services/tools
        health_check_service = HealthCheckService(
            health_check_repository=health_check_repository,
        )
        
        return ServiceState(
            **state,
            db_engine=db_engine,
            health_check_repository=health_check_repository,
            health_check_service=health_check_service,
        )

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        # self.logger.info("detector_service_stopped")
