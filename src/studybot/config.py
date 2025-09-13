"""Create cpnfiguration class."""

import logging
from pathlib import Path

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
