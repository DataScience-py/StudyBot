"""Create cpnfiguration class."""

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
