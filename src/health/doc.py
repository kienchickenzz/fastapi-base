"""
OpenAPI documentation tags cho Health module.
"""
from src.base.doc import Tag, TagEnum


class Tags(TagEnum):
    """Tags cho Health endpoints."""

    HEALTH = Tag(name="Health", description="Health management endpoints")
