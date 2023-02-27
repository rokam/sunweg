"""Sunweg API util."""
from enum import Enum


class Status(Enum):
    """Status enum."""

    OK = 0
    WARN = 2
    ERROR = 1


class SingletonMeta(type):
    """Singleton meta."""

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        """Handle singleton creation."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
