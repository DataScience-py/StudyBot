"""Create cpnfiguration class."""

from pathlib import Path

from pydantic import BaseModel

BASE_PATH = Path(__file__).parent.parent


class Config(BaseModel):
    """
    cofig class.

    Parameters
    ----------
    BaseModel : BaseModel
        BaseModel class. Pydantic class.
    """
