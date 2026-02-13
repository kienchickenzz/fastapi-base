"""
Entry point của FastAPI application.
"""

import argparse
import logging
from pathlib import Path

import uvicorn

from src.logger.LoggerConfig import LoggerConfig
from src.logger.LoggerFactory import LoggerFactory


# Khởi tạo logger singleton ngay khi module được load
_logger_config = LoggerConfig(project_root=Path(__file__).parent.parent)
_logger_factory = LoggerFactory(_logger_config)
logger = _logger_factory.get_instance()

 # TODO: Thêm note bàn luận về kiến trúc, cách tổ chức code,
 # cách tổ chức hiện tại không thể scale được theo hướng module hóa vì 
 # 1 module = 1 app FastAPI, cần refactor lại để có thể scale theo module mà không cần nhiều app FastAPI
def main() -> None:
    """
    Khởi chạy server với uvicorn.
    """
    parser = argparse.ArgumentParser(description="FastAPI Application Server")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Chạy ở chế độ debug với hot reload",
    )
    args = parser.parse_args()

    logger.info("Starting application...")
    logger.info(f"Debug mode: {args.debug}")

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=args.debug,
        log_level="debug" if args.debug else "info",
        ws="none",
    )


if __name__ == "__main__":
    main()
