"""Sunweg API plant."""

from datetime import datetime
import warnings

from .device import Inverter


class Plant:
    """Plant details."""

    def __init__(
        self,
        id: int,
        name: str,
        total_power: float,
        kwh_per_kwp: float,
        performance_rate: float,
        saving: float,
        today_energy: float,
        today_energy_metric: str,
        total_energy: float,
        total_carbon_saving: float,
        last_update: datetime | None,
    ) -> None:
        """
        Initialize Plant.

        :param id: plant id
        :type id: int
        :param name: plant name
        :type name: str
        :param total_power: plant total power
        :type total_power: float
        :param kwh_per_kwp: plant kWh/kWp
        :type kwh_per_kwp: float
        :param performance_rate: plant performance rate
        :type performance_rate: float
        :param saving: total saving in R$
        :type saving: float
        :param today_energy: today generated energy
        :type today_energy: float
        :param today_energy_metric: today generated energy metric
        :type today_energy_metric: str
        :param total_energy: total generated energy in kWh
        :type total_energy: float
        :param total_carbon_saving: total of CO2 saved
        :type total_carbon_saving: float
        :param last_update: when the data was updated
        :type last_update: datetime | None
        """
        self._id = id
        self._name = name
        self._total_power = total_power
        self._kwh_per_kwp = kwh_per_kwp
        self._performance_rate = performance_rate
        self._saving = saving
        self._today_energy = today_energy
        self._today_energy_metric = today_energy_metric
        self._total_energy = total_energy
        self._total_carbon_saving = total_carbon_saving
        self._last_update = last_update
        self._inverters: list[Inverter] = []

    @property
    def id(self) -> int:
        """
        Get plant id.

        :return: plant id
        :rtype: int
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Get plant name.

        :return: plant name
        :rtype: str
        """
        return self._name

    @property
    def total_power(self) -> float:
        """
        Get plant total power.

        :return: plant total power
        :rtype: float
        """
        return self._total_power

    @property
    def kwh_per_kwp(self) -> float:
        """
        Deprecated as API v2 doesn't return it anymore.
        Get plant kWh/kWp.

        :return: plant kWh/kWp
        :rtype: float
        """
        warnings.warn(
            "The 'kwh_per_kwp' property is deprecated and will return 0.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._kwh_per_kwp

    @property
    def performance_rate(self) -> float:
        """
        Deprecated as API v2 doesn't return it anymore.
        Get plant performance rate.

        :return: plant performance rate
        :rtype: float
        """
        warnings.warn(
            "The 'performance_rate' property is deprecated and will return 0.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._performance_rate

    @property
    def saving(self) -> float:
        """
        Get plant saving in R$.

        :return: plant saving in R$
        :rtype: float
        """
        return self._saving

    @property
    def today_energy(self) -> float:
        """
        Get plant today generated energy.

        :return: plant today generated energy
        :rtype: float
        """
        return self._today_energy

    @property
    def today_energy_metric(self) -> str:
        """
        Get plant today generated energy metric.

        :return: plant today generated energy metric
        :rtype: str
        """
        return self._today_energy_metric

    @property
    def total_energy(self) -> float:
        """
        Get plant total generated energy in kWh.

        :return: plant total generated energy in kWh
        :rtype: float
        """
        return self._total_energy

    @property
    def total_carbon_saving(self) -> float:
        """
        Get plant total of CO2 saved.

        :return: plant total of CO2 saved
        :rtype: float
        """
        return self._total_carbon_saving

    @property
    def last_update(self) -> datetime | None:
        """
        Get when the plant data was updated.

        :return: when the plant data was updated
        :rtype: datetime | None
        """
        return self._last_update

    @property
    def inverters(self) -> list[Inverter]:
        """
        Get list of plant's inverters.

        :return: list of inverters
        :rtype: list[Inverter]
        """
        return self._inverters

    def __str__(self) -> str:
        """Cast Plant to str."""
        return str(self.__class__) + ": " + str(self.__dict__)
