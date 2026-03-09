"""
Entry point của FastAPI application.
"""
import argparse
from os import environ
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

from src.config import Config
from src.logger.LoggerConfig import LoggerConfig
from src.logger.LoggerFactory import LoggerFactory


# Khởi tạo logger singleton ngay khi module được load
_logger_config = LoggerConfig(project_root=Path(__file__).parent.parent)
_logger_factory = LoggerFactory(_logger_config)
logger = _logger_factory.get_instance()



def run_server(args: argparse.Namespace) -> None:
    """
    Khởi chạy FastAPI server với uvicorn.

    Args:
        args (argparse.Namespace): Parsed arguments chứa debug flag.
    """
    # Load env và config
    load_dotenv('.env')
    config = Config(environ)

    root_path = config.get_config("ROOT_PATH", "")

    logger.info("Starting application...")
    logger.info(f"Debug mode: {args.debug}")
    logger.info(f"Root path: {root_path}")

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=args.debug,
        log_level="debug" if args.debug else "info",
        ws="none",
    )


def main() -> None:
    """
    Entry point chính, parse arguments và dispatch subcommand.
    """
    parser = argparse.ArgumentParser(
        description="FastAPI Application Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python -m src                  # Start server (default)
  uv run python -m src server           # Start server explicitly
  uv run python -m src server --debug   # Start server in debug mode
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # =================================================================
    # Subcommand: server (default)
    # =================================================================
    server_parser = subparsers.add_parser(
        "server",
        help="Start the FastAPI server",
    )
    server_parser.add_argument(
        "--debug",
        action="store_true",
        help="Chạy ở chế độ debug với hot reload",
    )
    server_parser.set_defaults(func=run_server)

    # Parse arguments
    args = parser.parse_args()

    # Nếu không có subcommand, mặc định chạy server
    if args.command is None:
        # Chạy server với default debug=False
        args.debug = False
        run_server(args)
    else:
        # Dispatch đến subcommand tương ứng
        args.func(args)


if __name__ == "__main__":
    main()

