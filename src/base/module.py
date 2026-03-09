"""
Interface module cho Composite Initializer Pattern.

Module này định nghĩa các interface và dataclass cần thiết để triển khai
pattern Composite Initializer, cho phép mỗi service module tự đăng ký
dependencies của mình mà không cần biết về các module khác.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine

from src.config import Config


@dataclass
class ModuleContext:
    """
    Shared resources được truyền từ AppInitializer xuống các Module.

    Context này chứa các tài nguyên dùng chung mà tất cả modules đều cần,
    cũng như cơ chế để các module chia sẻ dependencies với nhau.

    Args:
        db_engine (AsyncEngine): Database engine đã khởi tạo từ EngineFactory
        config (Config): Configuration object chứa env variables
        shared_repositories (dict): Repositories từ các modules đã khởi tạo trước.
            Dùng để giải quyết cross-module dependencies.
            Ví dụ: AuthModule cần UserRepository từ UserModule.
    """

    db_engine: AsyncEngine
    config: Config
    shared_repositories: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModuleDependencies:
    """
    Dependencies mà Module đăng ký, sẽ được inject vào request.state.

    Mỗi module trả về object này sau khi khởi tạo, chứa các services
    và repositories mà module đó cung cấp.

    Args:
        services (dict): Mapping tên -> service instance.
            Ví dụ: {"user_service": UserService(...)}
        repositories (dict): Mapping tên -> repository instance.
            Ví dụ: {"user_repository": UserRepository(...)}
    """

    services: dict[str, Any] = field(default_factory=dict)
    repositories: dict[str, Any] = field(default_factory=dict)


class IModule(ABC):
    """
    Interface cho mỗi service module.

    Mỗi module implement interface này để đăng ký dependencies.
    Module KHÔNG tạo FastAPI app, chỉ khởi tạo và trả về dependencies.

    Workflow:
        1. AppInitializer tạo ModuleContext với shared resources
        2. AppInitializer gọi module.initialize(context) theo thứ tự
        3. Module khởi tạo repositories và services của mình
        4. Module trả về ModuleDependencies
        5. AppInitializer cập nhật shared_repositories để module sau có thể dùng
    """

    @abstractmethod
    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo và trả về dependencies của module.

        Args:
            context (ModuleContext): Shared resources từ AppInitializer.
                Bao gồm db_engine, config, và shared_repositories từ
                các modules đã khởi tạo trước.

        Returns:
            ModuleDependencies: Services và repositories của module này.
        """
        pass

    async def shutdown(self) -> None:
        """
        Cleanup khi app shutdown.

        Override method này nếu module cần cleanup resources
        (đóng connections, flush buffers, etc.)
        """
        pass
