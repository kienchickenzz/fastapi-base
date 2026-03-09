"""
Module định nghĩa base model cho SQLAlchemy ORM.
Cung cấp các trường cơ bản và cấu hình chung cho tất cả models.
"""
from datetime import datetime

from sqlalchemy import Integer, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class cho tất cả SQLAlchemy models.

    Cung cấp các trường chung:
    - id: Primary key tự động tăng
    - created_at: Thời điểm tạo record
    - updated_at: Thời điểm cập nhật record gần nhất

    Kế thừa từ AsyncAttrs để hỗ trợ async operations
    và DeclarativeBase cho ORM mapping.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
