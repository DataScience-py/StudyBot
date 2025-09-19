"""Create cpnfiguration class."""

import logging
from collections.abc import Callable
from pathlib import Path
from time import perf_counter
from typing import ClassVar, ParamSpec, TypeVar

from pydantic_settings import BaseSettings, SettingsConfigDict

from .text import (
    ANSWER_QESTION_TEXT,
    CHOICE_NUMBER_TEXT,
    CHOICE_SUBJECTS_TEXT,
    CHOICE_TASK_TEXT,
    CHOICE_TASK_TEXT_WRITE,
    FAILED_ANSWER,
    SHOW_CORRECT_ANSWER,
    START_TEXT,
)

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

    RAM_TIME_MIN: ClassVar[int] = 10
    INTERVAL_SAVE_RAM_SEC: ClassVar[int] = 1200
    LAST_USE_RAM: ClassVar[str] = "LAST_USE_RAM"
    RUN: bool = False
    CHECK_INTERVAL: ClassVar[int] = 60
    ID_TASKS_FILE: str = "ID_TASK.txt"
    TASK_ANSWER: str = "TASK_ANSWER"
    TASK_TEXT: str = "TASK_TEXT"
    ID_TASK_FILE: str = "ID_TASK_FILE.txt"
    CHOICE_SUBJECTS_TEXT: str = "CHOICE_SUBJECTS_TEXT"
    CHOICE_NUMBER_TEXT: str = "CHOICE_NUMBER_TEXT {}"
    CHOICE_TASK_TEXT: str = "CHOICE_TASK_TEXT {} {}"
    FILE_NOT_FOUND_ERROR: str = "FILE_NOT_FOUND_ERROR with index {}"
    CHOICE_TASK_TEXT_WRITE: str = (
        "CHOICE_TASK_TEXT_WRITE {} {} Write a number start from 1 to {}"
    )
    START_TEXT: str = "START_TEXT"
    SUBJECTS_START_QERY: str = "SUBJECTS_"
    NUMBER_START_QERY: str = "NUMBER_"
    TASK_START_QERY: str = "TASK_"
    NUMBER: ClassVar[str] = "NUMBER"
    TASK: ClassVar[str] = "TASK"
    SUBJECTS: ClassVar[str] = "SUBJECTS"
    ANSWER_QESTION_TEXT: str = "ANSWER_QESTION_TEXT {} {} {} {}"
    LAST_ANSWER: ClassVar[str] = "LAST_ANSWER"
    MAX_LEN_TAKS: int = 40
    TASK_IMG: str = "TASK_IMG"
    WAIT_TASK_NUMBER: str = "WAIT_TASK_NUMBER"
    ATTEMPTS: str = "ATTEMPTS"
    FAILED_ANSWER: str = "FAILED_ANSWER {}"
    MAX_ATTEMPS: int = 3
    SHOW_CORRECT_ANSWER: str = "SHOW_CORRECT_ANSWER {}"

    model_config = SettingsConfigDict(env_file=BASE_PATH.parent / ".env")


config = Config(
    START_TEXT=START_TEXT,
    CHOICE_SUBJECTS_TEXT=CHOICE_SUBJECTS_TEXT,
    CHOICE_NUMBER_TEXT=CHOICE_NUMBER_TEXT,
    CHOICE_TASK_TEXT_WRITE=CHOICE_TASK_TEXT_WRITE,
    CHOICE_TASK_TEXT=CHOICE_TASK_TEXT,
    ANSWER_QESTION_TEXT=ANSWER_QESTION_TEXT,
    FAILED_ANSWER=FAILED_ANSWER,
    SHOW_CORRECT_ANSWER=SHOW_CORRECT_ANSWER,
)


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
    file_handler.setLevel(logging.DEBUG)
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
