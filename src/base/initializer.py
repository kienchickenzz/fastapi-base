"""
Application lifecycle management module.
Quản lý startup/shutdown và validation cho FastAPI app.
"""

from types import TracebackType
from typing import Optional, Type, Mapping, Any

from fastapi import FastAPI

from src.config import Config
from src.base.engine_factory import EngineFactory


class State(Mapping):
    """
    Chứa tất cả dependencies có thể inject vào Routers.

    Class này implement Mapping interface để cho phép
    truy cập dependencies như dictionary.
    """

    config: Config

    def __init__(self, /, **kwargs: Any):
        """
        Khởi tạo State với các dependencies.

        Args:
            **kwargs (Any): Các dependencies cần lưu trữ.
        """
        self.__dict__.update(kwargs)

    def __getitem__(self, item):
        """
        Lấy dependency theo key.

        Args:
            item: Key của dependency.

        Returns:
            Dependency value tương ứng với key.
        """
        return self.__dict__[item]

    def __iter__(self):
        """
        Iterator cho tất cả dependency keys.

        Returns:
            Iterator của các keys.
        """
        return self.__dict__.__iter__()

    def __len__(self):
        """
        Số lượng dependencies trong State.

        Returns:
            int: Số lượng dependencies.
        """
        return self.__dict__.__len__()


class Initializer:
    """
    Base class quản lý lifecycle của FastAPI application.

    Thực hiện setup, validation và cleanup cho app.
    Có thể được extend để thêm custom initialization logic.
    """

    _DOCS_ENDPOINT = "/"
    _HEALTH_ENDPOINT = "/health"
    _OPENAPI_VERSION = "3.0.2"

    def __init__(self, app: FastAPI, config: Optional[Config] = None) -> None:
        """
        Khởi tạo Initializer.

        Args:
            app (FastAPI): FastAPI application instance.
            config (Optional[Config]): Config instance. Nếu None sẽ tạo mới.
        """
        self.config: Config = config if config else Config()
        self._app = app
        self.engine_factory = EngineFactory(config=self.config)

    async def __aenter__(self) -> State:
        """
        Async context manager entry. Setup app và khởi tạo dependencies.

        Thực hiện các bước:
        1. Tạo State với config
        2. Setup app với version và debug mode
        3. Validate OpenAPI specification
        4. Validate required endpoints
        5. Khởi tạo database engine factory

        Returns:
            State: State instance chứa các dependencies.
        """
        state = State(
            config=self.config,
        )

        # FastAPI setup and validation
        self._setup_app()
        self._validate_openapi()
        self._validate_endpoints()

        # Database setup
        await self.engine_factory.__aenter__()

        # self.logger.info("service_initialized")

        return state

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        """
        Async context manager exit. Cleanup resources.

        Args:
            exc_type (Optional[Type[BaseException]]): Exception type nếu có.
            exc_val (Optional[BaseException]): Exception value nếu có.
            exc_tb (Optional[TracebackType]): Traceback nếu có.
        """
        # self.logger.info("service_shutting_down")
        await self.engine_factory.__aexit__(exc_type, exc_val, exc_tb)

    def _setup_app(self) -> None:
        """
        Setup FastAPI app với config từ environment.

        Cấu hình version từ RELEASE env var và debug mode từ DEBUG env var.
        """
        self._app.version = self.config.get_config("RELEASE", "")
        self._app.debug = self.config.get_bool("DEBUG", False)

    def _validate_openapi(self) -> None:
        """
        Validate OpenAPI specification của app.

        Kiểm tra các trường bắt buộc trong OpenAPI spec:
        - info.title (không được là "FastAPI" mặc định)
        - info.description
        - info.contact.name
        - info.contact.url

        Raises:
            AssertionError: Nếu thiếu bất kỳ trường bắt buộc nào.
        """
        spec = self._app.openapi()

        assert "info" in spec, "openapi_spec_info_missing"
        assert "title" in spec["info"], "openapi_spec_title_missing"
        assert "description" in spec["info"], "openapi_spec_description_missing"
        assert "contact" in spec["info"], "openapi_spec_contact_missing"
        assert "name" in spec["info"]["contact"], "openapi_spec_contact_name_missing"
        assert "url" in spec["info"]["contact"], "openapi_spec_contact_url_missing"

        assert "FastAPI" != spec["info"]["title"], "openapi_spec_title_missing"
        # assert spec["info"]["contact"]["url"].startswith(""), "openapi_spec_url_invalid_host"

        if spec["openapi"] != self._OPENAPI_VERSION:
            # self.logger.warning(
            #     "openapi_version_overwritten",
            #     original_version=spec["openapi"],
            #     supported_versions=self._OPENAPI_VERSION,
            # )
            spec["openapi"] = self._OPENAPI_VERSION

    def _validate_endpoints(self) -> None:
        """
        Validate các endpoints bắt buộc của app.

        Kiểm tra sự tồn tại của:
        - Health endpoint (/health)
        - Docs endpoint (/)

        Raises:
            AssertionError: Nếu thiếu endpoint bắt buộc.
        """
        endpoints = [route.path for route in self._app.routes]
        assert self._HEALTH_ENDPOINT in endpoints, "health_endpoint_missing"
        assert self._DOCS_ENDPOINT in endpoints, "docs_endpoint_missing"
