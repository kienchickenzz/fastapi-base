"""
Module cung cấp dependency injection utilities cho FastAPI.
Cho phép inject dependencies từ request.state vào routers.
"""
from typing import Any

from fastapi import Request, params
from starlette import datastructures
from typing_extensions import Annotated, Doc


def Injects(  # noqa: N802
    dependency: Annotated[
        str,
        Doc("The name of dependency, defined in State, that will be injected in the router."),
    ],
    *,
    use_cache: Annotated[
        bool,
        Doc(
            """
                By default, after a dependency is called the first time in a request, if
                the dependency is declared again for the rest of the request (for example
                if the dependency is needed by several dependencies), the value will be
                re-used for the rest of the request.

                Set `use_cache` to `False` to disable this behavior and ensure the
                dependency is called again (if declared more than once) in the same request.
                """
        ),
    ] = True,
) -> Any:
    """
    Inject một dependency từ request.state vào router.

    Sử dụng như FastAPI Depends() nhưng lấy dependency từ State
    thay vì gọi function.

    Args:
        dependency (str): Tên của dependency trong State.
        use_cache (bool): Cache kết quả trong request. Mặc định True.

    Returns:
        Any: Dependency value từ request.state.

    Raises:
        RuntimeError: Nếu dependency không tồn tại trong state.

    Example:
        >>> @router.get("/users")
        ... async def get_users(
        ...     user_service: UserService = Injects("user_service")
        ... ):
        ...     return await user_service.get_all()
    """

    def _inject_from_state(request: Request) -> Any:
        # Sử dụng getattr với default=None để tránh exception chaining
        # từ Starlette State.__getattr__ (KeyError → AttributeError)
        value = getattr(request.state, dependency, None)
        if value is None:
            raise RuntimeError(
                f"Dependency '{dependency}' not found in request.state. "
                f"Ensure it is registered in the appropriate Module and "
                f"added to AppInitializer._modules."
            )
        return value

    return params.Depends(dependency=_inject_from_state, use_cache=use_cache)


def InjectState(  # noqa: N802
    *,
    use_cache: Annotated[
        bool,
        Doc(
            """
                By default, after a dependency is called the first time in a request, if
                the dependency is declared again for the rest of the request (for example
                if the dependency is needed by several dependencies), the value will be
                re-used for the rest of the request.

                Set `use_cache` to `False` to disable this behavior and ensure the
                dependency is called again (if declared more than once) in the same request.
                """
        ),
    ] = True,
) -> Any:
    """
    Inject toàn bộ request.state vào router.

    Hữu ích khi cần truy cập nhiều dependencies cùng lúc
    hoặc khi dependency name chỉ biết lúc runtime.

    Args:
        use_cache (bool): Cache kết quả trong request. Mặc định True.

    Returns:
        Any: Starlette State object chứa tất cả dependencies.

    Example:
        >>> @router.get("/info")
        ... async def get_info(state: State = InjectState()):
        ...     return {"config": state.config}
    """

    def _inject_state(request: Request) -> datastructures.State:
        return request.state

    return params.Depends(dependency=_inject_state, use_cache=use_cache)
