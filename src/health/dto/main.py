from datetime import datetime

from pydantic import BaseModel, field_serializer

from src.base.dto.main import PaginatedRequestBase, PaginatedResponseBase, ResponseBase

class HealthCheckRequest(PaginatedRequestBase):
    pass

class HealthCheckDto(ResponseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_dates(self, value: datetime) -> str:
        return value.isoformat() if value else None # type: ignore

class HealthCheckResponseDto(PaginatedResponseBase):
    health_checks: list[HealthCheckDto]
