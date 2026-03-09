"""
Module định nghĩa base DTOs cho API requests và responses.
Cung cấp cấu hình chung và pagination support.
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from humps import camelize
from fastapi import Query


class RequestBase(BaseModel):
    """
    Base class cho tất cả request DTOs.

    Cấu hình:
    - frozen: Immutable sau khi tạo
    - alias_generator: Tự động convert sang camelCase
    - populate_by_name: Cho phép dùng cả snake_case và camelCase
    - validate_assignment: Validate khi gán giá trị
    - extra='forbid': Không cho phép fields không khai báo
    """
    model_config = ConfigDict(
        frozen=True,
        alias_generator=camelize,
        populate_by_name=True,
        validate_assignment=True,
        extra='forbid',
    )

class PaginatedRequestBase(RequestBase):
    """
    Base class cho request DTOs có pagination.

    Attributes:
        target_page (int): Số trang cần lấy (bắt đầu từ 1).
        page_size (int): Số items mỗi trang (1-100).
    """

    model_config = ConfigDict(
        frozen=True,
        alias_generator=camelize,
        populate_by_name=True,
        validate_assignment=True,
        extra='forbid',
    )

    target_page: int = Field(
        default=1,
        ge=1,  # Greater than or equal to 1
        description="Target page number"
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,  # Limit tối đa
        description="Number of items per page"
    )

    # Custom validator
    @field_validator('page_size')
    @classmethod
    def validate_page_size(cls, v):
        """
        Validate page_size không vượt quá 100.

        Args:
            v: Giá trị page_size cần validate.

        Returns:
            int: Giá trị đã validate.

        Raises:
            ValueError: Nếu page_size > 100.
        """
        if v > 100:
            raise ValueError("Page size cannot exceed 100")
        return v

    @classmethod
    def as_query(
        cls,
        target_page: int = Query(
            default=1,
            alias="targetPage",
            ge=1,
            description="Target page number"
        ),
        page_size: int = Query(
            default=10,
            alias="pageSize",
            ge=1,
            le=100,
            description="Number of items per page"
        )
    ) -> "PaginatedRequestBase":
        """
        Tạo instance từ query parameters.

        Sử dụng làm dependency trong FastAPI endpoint để parse
        pagination params từ query string.

        Args:
            target_page (int): Số trang từ query param 'targetPage'.
            page_size (int): Số items từ query param 'pageSize'.

        Returns:
            PaginatedRequestBase: Instance với pagination params.

        Example:
            >>> @router.get("/items")
            ... async def get_items(
            ...     pagination: PaginatedRequestBase = Depends(PaginatedRequestBase.as_query)
            ... ):
            ...     return await service.get_list(pagination.target_page, pagination.page_size)
        """
        return cls(target_page=target_page, page_size=page_size)

class ResponseBase(BaseModel):
    """
    Base class cho tất cả response DTOs.

    Cấu hình:
    - frozen: Immutable sau khi tạo
    - alias_generator: Tự động convert sang camelCase
    - populate_by_name: Cho phép dùng cả snake_case và camelCase
    - validate_assignment: Validate khi gán giá trị
    - extra='ignore': Bỏ qua fields không khai báo
    - from_attributes: Cho phép tạo từ ORM model
    """

    model_config = ConfigDict(
        frozen=True,
        alias_generator=camelize,
        populate_by_name=True,
        validate_assignment=True,
        extra='ignore',
        from_attributes=True
    )


class PaginatedResponseBase(ResponseBase):
    """
    Base class cho response DTOs có pagination.

    Attributes:
        current_page (int): Trang hiện tại.
        total_pages (int): Tổng số trang.
        page_size (int): Số items mỗi trang.
    """

    current_page: int
    total_pages: int
    page_size: int
