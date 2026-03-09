"""
Module cung cấp base classes cho OpenAPI documentation tags.
Định nghĩa Tag và TagEnum để tổ chức API endpoints trong Swagger.
"""
from enum import Enum
from typing import Any, Dict, List, Optional


class Tag:
    """
    Class đại diện cho một OpenAPI tag.

    Tag được sử dụng để nhóm và mô tả các API endpoints
    trong OpenAPI/Swagger documentation.

    Args:
        name (str): Tên của tag hiển thị trong Swagger.
        description (Optional[str]): Mô tả chi tiết về tag.
        url (Optional[str]): URL tài liệu bên ngoài liên quan.
    """

    name: str
    description: Optional[str]
    url: Optional[str]

    def __init__(self, name: str, description: Optional[str] = None, url: Optional[str] = None):
        """
        Khởi tạo Tag instance.

        Args:
            name (str): Tên của tag hiển thị trong Swagger.
            description (Optional[str]): Mô tả chi tiết về tag.
            url (Optional[str]): URL tài liệu bên ngoài liên quan.
        """
        self.name = name
        self.description = description
        self.url = url


class TagEnum(Tag, Enum):
    """
    Enum to organize Tag documentation used by Routers, OpenAPI and Swagger.

    You can create tags following the example bellow:

    >>> class Tags(TagEnum):
    ...     TAG_1 = Tag(
    ...         name="Tag One",
    ...         description="My custom Tag One",
    ...         url="https://tags.staging.vrff.io/",
    ...     )
    ...     TAG_2 = Tag(name="Tag Two", description="My custom Tag Two")

    Once a Tag is defined, it can be injected into Routers to improve Swagger readability:

    >>> my_router = APIRouter(tags=[Tags.TAG_1])
    """

    def __init__(self, *args, **kwargs) -> None:
        # pylint: disable=super-init-not-called
        assert len(args) == 1, "only_one_tag_allowed"
        assert len(kwargs) == 0, "no_extra_parameters_allowed"
        assert isinstance(args[0], Tag), "only_tag_allowed"

        self._value_ = args[0].name
        self._detail_ = args[0]

    @property
    def detail(self) -> Tag:
        """The tag detail of the Enum member."""
        return self._detail_

    @classmethod
    def get_docs(cls) -> List[Dict[str, Any]]:
        """
        Lấy danh sách documentation cho tất cả tags trong enum.

        Returns:
            List[Dict[str, Any]]: Danh sách các tag descriptions
                theo format OpenAPI specification.
        """
        return [cls._get_tag_description(item.detail) for item in cls]

    @staticmethod
    def _get_tag_description(tag: Tag) -> Dict[str, Any]:
        """
        Chuyển đổi Tag thành dictionary format cho OpenAPI.

        Args:
            tag (Tag): Tag cần chuyển đổi.

        Returns:
            Dict[str, Any]: Dictionary chứa name, description
                và externalDocs (nếu có url).
        """
        result: Dict[str, Any] = {"name": tag.name, "description": tag.description}

        if tag.url:
            result["externalDocs"] = {"url": tag.url}

        return result
