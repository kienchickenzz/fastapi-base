"""
Generic repository module cung cấp các CRUD operations cơ bản cho SQLAlchemy models.
"""

from abc import ABC
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Optional, Sequence, Type, TypeVar, Generic

from sqlalchemy import insert, select, update, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.engine import RowMapping

from src.base.database.model.base import Base


T = TypeVar("T", bound=Base)


class Repository(ABC, Generic[T]):
    """
    Abstract repository cung cấp các CRUD operations cho SQLAlchemy models.

    Delete method không được cung cấp mặc định vì khuyến khích immutability,
    subclass có thể implement khi cần thiết.
    """

    def __init__(self, engine: AsyncEngine, db_model: Type[T]):
        """
        Khởi tạo repository.

        Args:
            engine (AsyncEngine): SQLAlchemy async engine
            db_model (Type[T]): SQLAlchemy model class
        """
        self._model = db_model
        self._engine = engine
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def _get_session(self) -> AsyncIterator[AsyncSession]:
        """
        Context manager để lấy database session.

        Yields:
            AsyncSession: SQLAlchemy async session
        """
        session = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_all(self) -> Sequence[T]:
        """
        Lấy tất cả entities từ database, sắp xếp theo id.

        Returns:
            Sequence[T]: Danh sách entities
        """
        async with self._get_session() as session:
            query = select(self._model).order_by(self._model.id)
            result = await session.scalars(query)
            return result.all()

    async def get_one(self, entity_id: int) -> Optional[T]:
        """
        Lấy một entity theo id.

        Args:
            entity_id (int): ID của entity

        Returns:
            Optional[T]: Entity hoặc None nếu không tìm thấy
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.id == entity_id)
            result = await session.scalars(query)
            return result.first()

    async def get_multiple(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[T], int]:
        """
        Lấy danh sách entities với pagination.

        Args:
            skip (int): Số records bỏ qua
            limit (int): Số records tối đa trả về (0 = không giới hạn)

        Returns:
            tuple[Sequence[T], int]: (danh sách entities, tổng số records)
        """
        async with self._get_session() as session:
            # Count total
            count_query = select(self._model)
            count_result = await session.scalars(count_query)
            total = len(count_result.all())

            # Fetch with pagination
            query = select(self._model).order_by(self._model.id).offset(skip)
            if limit > 0:
                query = query.limit(limit)

            result = await session.scalars(query)
            return result.all(), total

    async def create(self, values: dict[str, Any]) -> T:
        """
        Tạo một entity mới.

        Args:
            values (dict[str, Any]): Dữ liệu entity

        Returns:
            T: Entity đã tạo
        """
        async with self._get_session() as session:
            query = insert(self._model).values(values).returning(self._model)
            result = await session.execute(query)
            entity = result.scalar_one()
            await session.commit()
            return entity

    async def update(self, entity_id: int, values: dict[str, Any]) -> Optional[T]:
        """
        Cập nhật một entity.

        Args:
            entity_id (int): ID của entity
            values (dict[str, Any]): Dữ liệu cập nhật

        Returns:
            Optional[T]: Entity đã cập nhật hoặc None nếu không tìm thấy
        """
        async with self._get_session() as session:
            query = (
                update(self._model)
                .where(self._model.id == entity_id)
                .values(values)
                .returning(self._model)
            )
            result = await session.execute(query)
            entity = result.scalar_one_or_none()
            await session.commit()
            return entity

    async def fetch_sql(
        self,
        sql: str,
        parameters: Optional[dict[str, Any]] = None,
    ) -> Sequence[RowMapping]:
        """
        Thực thi SELECT query và trả về kết quả.

        Args:
            sql (str): Raw SQL query
            parameters (Optional[dict[str, Any]]): Query parameters

        Returns:
            Sequence[RowMapping]: Kết quả query
        """
        async with self._get_session() as session:
            query = text(sql)
            result = await session.execute(query, parameters or {})
            return result.mappings().all()

    async def execute_sql(
        self,
        sql: str,
        parameters: Optional[dict[str, Any]] = None,
    ) -> int:
        """
        Thực thi INSERT/UPDATE/DELETE query.

        Args:
            sql (str): Raw SQL statement
            parameters (Optional[dict[str, Any]]): Query parameters

        Returns:
            int: Số rows bị ảnh hưởng
        """
        async with self._get_session() as session:
            query = text(sql)
            result = await session.execute(query, parameters or {})
            await session.commit()
            return result.rowcount
