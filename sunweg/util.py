"""Sunweg API util."""

from datetime import date
from enum import Enum


class Status(Enum):
    """Status enum."""

    OK = 0
    WARN = 2
    ERROR = 1


class ProductionStats:
    """Energy production statistics"""

    def __init__(self, date: date, production: float, prognostic: float) -> None:
        """
        Initialize energy production statistics.

        :param date: statistics date
        :type date: date
        :param production: statistics production in kWh
        :type production: float
        :param prognostic: statistics expected production in kWh
        """
        self._date = date
        self._production = production
        self._prognostic = prognostic

    @property
    def date(self) -> date:
        """Get date."""
        return self._date

    @property
    def production(self) -> float:
        """Get energy production in kWh."""
        return self._production

    @property
    def prognostic(self) -> float:
        """Get expected energy production in kWh."""
        return self._prognostic

    def __str__(self) -> str:
        """Cast Phase to str."""
        return str(self.__class__) + ": " + str(self.__dict__)
