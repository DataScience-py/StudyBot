"""Create cpnfiguration class."""

import logging
from collections.abc import Callable
from pathlib import Path
from time import perf_counter
from typing import ParamSpec, TypeVar

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).parent.parent


class Config(BaseSettings):
    """
    cofig class.

    Parameters
    ----------
    BaseModel : BaseModel
        BaseModel class. Pydantic class.
    """

    BASE_PATH: Path = BASE_PATH

    TELEGRAM_TOKEN: str = ""

    model_config = SettingsConfigDict(env_file=BASE_PATH.parent / ".env")


config = Config()


def get_logger(
    name: str = "StudyBot",
    level: int = logging.INFO,
) -> logging.Logger:
    """Create logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level=level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    file_handler = logging.FileHandler("studybot.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    cmd_handler = logging.StreamHandler()
    cmd_handler.setFormatter(formatter)
    logger.addHandler(cmd_handler)
    return logger


P = ParamSpec("P")
T = TypeVar("T")


def time_logger(
    logger: logging.Logger,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    time_logger decorator.

    Parameters
    ----------
    logger : logging.Logger
        write log to file and console.

    Returns
    -------
    Callable[[Callable[P, T]], Callable[P, T]]
        function decorator.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            s = perf_counter()
            logger.debug("Start %s", func.__name__)
            result = func(*args, **kwargs)
            logger.debug(
                "Finish %s with seconds %s",
                func.__name__,
                perf_counter() - s,
            )
            return result

        return wrapper

    return decorator
