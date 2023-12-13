"""Sunweg API util."""
from enum import Enum


class Status(Enum):
    """Status enum."""

    OK = 0
    WARN = 2
    ERROR = 1
