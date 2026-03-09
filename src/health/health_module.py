"""
Module đăng ký dependencies cho Health service.

HealthModule là module độc lập, không có cross-module dependency.
Cung cấp health check functionality cho application.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.health.database.repository.health import HealthCheckRepository
from src.health.service.health_check.main import HealthCheckService


@dataclass
class HealthModule(IModule):
    """
    Module khởi tạo Health service và repositories.

    Dependencies được cung cấp:
        - health_check_repository: HealthCheckRepository instance
        - health_check_service: HealthCheckService instance

    Cross-module dependencies: Không có
    """

    _repository: HealthCheckRepository | None = None
    _service: HealthCheckService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo Health repositories và service.

        Args:
            context (ModuleContext): Chứa db_engine, config, và shared_repositories

        Returns:
            ModuleDependencies: health_check_repository, health_check_service
        """
        # Khởi tạo repository
        self._repository = HealthCheckRepository(engine=context.db_engine)

        # Khởi tạo service
        self._service = HealthCheckService(
            health_check_repository=self._repository,
        )

        return ModuleDependencies(
            services={"health_check_service": self._service},
            repositories={"health_check_repository": self._repository},
        )
