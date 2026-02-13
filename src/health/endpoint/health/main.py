"""
Health check endpoints module.
Cung cấp các API endpoints để kiểm tra trạng thái database.
"""

import logging

from fastapi import APIRouter, Depends

from src.base.dependency_injection import Injects
from src.health.doc import Tags
from src.health.service.health_check.main import HealthCheckService
from src.health.dto.main import (
    DbHealthCheckRequest,
    DbHealthCheckDto,
    DbHealthCheckResponseDto,
    DbHealthCheckCreateResponse,
)


logger = logging.getLogger("app")

router = APIRouter(tags=[Tags.HEALTH], prefix="/health")


@router.post(
    path="/db",
    response_model=DbHealthCheckCreateResponse,
    summary="Database Health Check",
    description="Tạo một health check entry mới để verify database connection",
    status_code=201,
)
async def check_db_health(
    health_check_service: HealthCheckService = Injects("health_check_service"),
) -> DbHealthCheckCreateResponse:
    """
    Tạo một health check entry mới trong database.

    Args:
        health_check_service (HealthCheckService): Service xử lý health check

    Returns:
        DbHealthCheckCreateResponse: Response chứa message và id
    """
    return await health_check_service.check_db_health()


@router.get(
    path="/db",
    response_model=DbHealthCheckResponseDto,
    summary="Get Database Health Checks",
    description="Lấy danh sách health check entries với pagination",
    status_code=200,
)
async def get_db_health(
    request: DbHealthCheckRequest = Depends(DbHealthCheckRequest.as_query),
    health_check_service: HealthCheckService = Injects("health_check_service"),
) -> DbHealthCheckResponseDto:
    """
    Lấy danh sách health check entries với pagination.

    Args:
        request (DbHealthCheckRequest): Request params (target_page, page_size)
        health_check_service (HealthCheckService): Service xử lý health check

    Returns:
        DbHealthCheckResponseDto: Danh sách health checks với thông tin pagination
    """
    return await health_check_service.get_db_health_checks(
        target_page=request.target_page,
        page_size=request.page_size,
    )


@router.get(
    path="/db/latest",
    response_model=DbHealthCheckDto,
    summary="Get Latest Database Health Check",
    description="Lấy health check entry mới nhất",
    status_code=200,
)
async def get_latest_db_health(
    health_check_service: HealthCheckService = Injects("health_check_service"),
) -> DbHealthCheckDto:
    """
    Lấy health check entry mới nhất.

    Args:
        health_check_service (HealthCheckService): Service xử lý health check

    Returns:
        DbHealthCheckDto: Health check entry mới nhất
    """
    return await health_check_service.get_latest_db_health_check()
