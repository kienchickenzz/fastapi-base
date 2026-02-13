from os import environ

from dotenv import load_dotenv

from src.base.app import create_fastapi_app
from src.config import Config
from src.health.health_initializer import HealthInitializer
from src.health.endpoint.main import main_router as router_health
from src.health.doc import Tags

load_dotenv('.env')
config = Config(environ)

app = create_fastapi_app(
    config=config,
    initializer=HealthInitializer,
    title="Minimal FastAPI Server",
    description="A minimal FastAPI server template with essential features",
    version="0.1.0",
    team_name="core",
    team_url="https://invalid-address.ee",
    openapi_tags=Tags.get_docs(),
)

# Service routes
app.include_router(router_health)
