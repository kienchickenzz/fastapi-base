from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, JSONResponse

from src.base.dependency_injection import Injects
from src.health.doc import Tags
from src.health.service.health_check.main import HealthCheckService
from src.health.dto.main import DbHealthCheckRequest

router = APIRouter(tags=[Tags.HEALTH], prefix="/health")

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post(
    path="/",
    summary="Health Check",
    description="Check service health status",
    status_code=200,
)
async def check_health(
    health_check_service: HealthCheckService = Injects("health_check_service"),
) -> PlainTextResponse:
    return PlainTextResponse("OK")

@router.post(
    path="/db",
    summary="Database Health Check",
    description="Check database health status",
    status_code=200,
)
async def check_db_health(
    health_check_service: HealthCheckService = Injects("health_check_service"),
) -> PlainTextResponse:
    await health_check_service.check_db_health()
    return PlainTextResponse("DB OK")

@router.get(
    path="/db",
    summary="Database Health Check",
    description="Check database health status",
    status_code=200,
)
async def get_db_health(
    request: DbHealthCheckRequest = Depends(DbHealthCheckRequest.as_query),
    health_check_service: HealthCheckService = Injects("health_check_service"),
):
    target_page = request.target_page
    page_size = request.page_size

    result = await health_check_service.get_db_health_checks(target_page, page_size)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)
