"""
Module quản lý configuration từ environment variables.
Cung cấp type-safe access và validation cho các config values.
"""
import getpass
import os
from typing import List, Mapping, Optional


TRUE_VALUES = ["1", "true", "yes"]
FALSE_VALUES = ["0", "false", "no"]


class ConfigError(ValueError):
    """Base exception cho các lỗi configuration."""

    pass


class ConfigValueMissingError(ConfigError):
    """Exception khi config value không tồn tại."""

    pass


class ConfigInvalidDefaultError(ConfigError):
    """Exception khi default value có type không hợp lệ."""

    pass


class ConfigInvalidValueError(ConfigError):
    """Exception khi config value không thể parse được."""

    pass


class Config:
    """
    Class quản lý configuration từ environment variables hoặc mapping.

    Cung cấp các methods để lấy config values với type validation
    và support cho required/optional values với default.

    Args:
        config_map (Optional[Mapping]): Mapping chứa config values.
            Mặc định sử dụng os.environ.
    """

    def __init__(self, config_map: Optional[Mapping] = None):
        """
        Khởi tạo Config instance.

        Args:
            config_map (Optional[Mapping]): Mapping chứa config values.
                Nếu None, sử dụng os.environ.
        """
        self.config_map = config_map if config_map is not None else os.environ
        self.config_map = {k: str(v) for k, v in self.config_map.items()}

    def require_config(self, name: str) -> str:
        """
        Lấy config value bắt buộc.

        Args:
            name (str): Tên của config key.

        Returns:
            str: Giá trị config.

        Raises:
            ConfigValueMissingError: Nếu config không tồn tại.
        """
        config = self.config_map.get(name)
        if config is None:
            raise ConfigValueMissingError(f"{name} isn't present in the config")
        return config

    def get_config(self, name: str, default: str) -> str:
        """
        Lấy config value với default fallback.

        Args:
            name (str): Tên của config key.
            default (str): Giá trị mặc định nếu không tìm thấy.

        Returns:
            str: Giá trị config hoặc default.
        """
        return self.config_map.get(name, default)

    def require_bool(self, name: str) -> bool:
        """
        Lấy config value boolean bắt buộc.

        Args:
            name (str): Tên của config key.

        Returns:
            bool: Giá trị boolean.

        Raises:
            ConfigValueMissingError: Nếu config không tồn tại.
            ConfigInvalidValueError: Nếu value không phải boolean hợp lệ.
        """
        if name not in self.config_map:
            raise ConfigValueMissingError(f"{name} isn't present in the config")

        value = self.config_map[name].lower()
        if value in TRUE_VALUES:
            return True
        if value in FALSE_VALUES:
            return False

        raise ConfigInvalidValueError(f"value of {name} is not valid boolean: '{value}'")

    def get_bool(self, name: str, default: bool) -> bool:
        """
        Lấy config value boolean với default fallback.

        Args:
            name (str): Tên của config key.
            default (bool): Giá trị mặc định nếu không tìm thấy.

        Returns:
            bool: Giá trị boolean hoặc default.

        Raises:
            ConfigInvalidDefaultError: Nếu default không phải boolean.
        """
        if not isinstance(default, bool):
            raise ConfigInvalidDefaultError("Default value must be boolean")

        try:
            return self.require_bool(name)
        except ConfigValueMissingError:
            return default

    def require_int(self, name: str) -> int:
        """
        Lấy config value integer bắt buộc.

        Args:
            name (str): Tên của config key.

        Returns:
            int: Giá trị integer.

        Raises:
            ConfigValueMissingError: Nếu config không tồn tại.
            ConfigInvalidValueError: Nếu value không phải integer hợp lệ.
        """
        if name not in self.config_map:
            raise ConfigValueMissingError(f"{name} isn't present in the config")

        value = self.config_map[name]
        try:
            return int(value)
        except ValueError as error:
            raise ConfigInvalidValueError(f"value of {name} is not valid int: '{value}'") from error

    def get_int(self, name: str, default: int) -> int:
        """
        Lấy config value integer với default fallback.

        Args:
            name (str): Tên của config key.
            default (int): Giá trị mặc định nếu không tìm thấy.

        Returns:
            int: Giá trị integer hoặc default.

        Raises:
            ConfigInvalidDefaultError: Nếu default không phải integer.
        """
        if not isinstance(default, int) or isinstance(default, bool):
            raise ConfigInvalidDefaultError("Default value must be int")

        try:
            return self.require_int(name)
        except ConfigValueMissingError:
            return default

    def require_float(self, name: str) -> float:
        """
        Lấy config value float bắt buộc.

        Args:
            name (str): Tên của config key.

        Returns:
            float: Giá trị float.

        Raises:
            ConfigValueMissingError: Nếu config không tồn tại.
            ConfigInvalidValueError: Nếu value không phải float hợp lệ.
        """
        if name not in self.config_map:
            raise ConfigValueMissingError(f"{name} isn't present in the config")

        value = self.config_map[name]
        try:
            return float(value)
        except ValueError as err:
            raise ConfigInvalidValueError(f"value of {name} is not valid float: '{value}'") from err

    def get_float(self, name: str, default: float) -> float:
        """
        Lấy config value float với default fallback.

        Args:
            name (str): Tên của config key.
            default (float): Giá trị mặc định nếu không tìm thấy.

        Returns:
            float: Giá trị float hoặc default.

        Raises:
            ConfigInvalidDefaultError: Nếu default không phải float.
        """
        if not isinstance(default, float):
            raise ConfigInvalidDefaultError("Default value must be float")
        try:
            return self.require_float(name)
        except ConfigValueMissingError:
            return default

    def require_list(self, name: str, separator: str) -> List[str]:
        """
        Lấy config value dạng list bắt buộc.

        Args:
            name (str): Tên của config key.
            separator (str): Ký tự phân cách các phần tử.

        Returns:
            List[str]: Danh sách các giá trị.

        Raises:
            ConfigValueMissingError: Nếu config không tồn tại.
            ConfigInvalidValueError: Nếu value không thể split được.
        """
        if name not in self.config_map:
            raise ConfigValueMissingError(f"{name} isn't present in the config")

        value = self.config_map[name]
        try:
            return value.split(separator)
        except ValueError as err:
            raise ConfigInvalidValueError(f"value of {name} is not valid list: '{value}'") from err

    def get_list(self, name: str, separator: str, default: List[str]) -> List[str]:
        """
        Lấy config value dạng list với default fallback.

        Args:
            name (str): Tên của config key.
            separator (str): Ký tự phân cách các phần tử.
            default (List[str]): Danh sách mặc định nếu không tìm thấy.

        Returns:
            List[str]: Danh sách các giá trị hoặc default.

        Raises:
            ConfigInvalidDefaultError: Nếu default không phải list of strings.
        """
        if not isinstance(default, List):
            raise ConfigInvalidDefaultError("Default value must be list")

        if not all(isinstance(item, str) for item in default):
            raise ConfigInvalidDefaultError("Default value must contain only strings")

        try:
            return self.require_list(name, separator)
        except ConfigValueMissingError:
            return default


def _get_username() -> str:
    """
    Lấy username của user hiện tại.

    Returns:
        str: Username hoặc "unknown" nếu không lấy được.
    """
    username = "unknown"
    try:
        username = getpass.getuser()
    except Exception:  # pylint: disable=broad-except
        pass
    return username
