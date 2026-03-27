"""
Entry point của FastAPI application.

Module này khởi tạo FastAPI app với các cấu hình:
- Load environment variables từ .env
- Setup AppInitializer để quản lý lifecycle
- Register tất cả routers từ các modules (health, ...)
- Cấu hình OpenAPI documentation với tags từ các modules
"""
from os import environ

from dotenv import load_dotenv

from src.config import Config

from src.base.app import create_fastapi_app
from src.initializer import AppInitializer

from src.health.endpoint.main import main_router as router_health
from src.health.doc import Tags as HealthTags


# Load environment variables
config = Config(environ)

# Lấy root_path từ config (prefix cho tất cả endpoints khi deploy sau reverse proxy)
root_path = config.get_config("ROOT_PATH", "")

# Combine OpenAPI tags từ tất cả modules
openapi_tags = (
    HealthTags.get_docs()
)

app = create_fastapi_app(
    config=config,
    initializer=AppInitializer,
    title="Minimal FastAPI Server",
    description="A minimal FastAPI server template with essential features",
    version="0.1.0",
    team_name="core",
    team_url="https://invalid-address.ee",
    openapi_tags=openapi_tags,
    root_path=root_path,
)

# Register routers từ các modules
app.include_router(router_health)
