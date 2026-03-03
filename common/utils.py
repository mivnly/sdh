import json
from logging import INFO, FileHandler, Formatter, Logger, getLogger
from pathlib import Path


def setup_logger(name: str, log_file: str) -> Logger:
    folder = Path("logs")

    logger = getLogger(name)
    logger.setLevel(INFO)
    logger.propagate = False

    logger.handlers.clear()

    handler = FileHandler(folder / log_file, mode="w", encoding="utf-8")
    formatter = Formatter(
        fmt="%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def pretty_print(msg):
    """Prettify given json. Disabled **ensure_ascii** parameter allows displaing more symbols (full Unicode)."""
    return json.dumps(msg, indent=4, ensure_ascii=False)
