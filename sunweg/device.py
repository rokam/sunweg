"""Sunweg API devices."""
from .util import Status


class Phase:
    """Phase details."""

    def __init__(
        self,
        name: str,
        voltage: float,
        amperage: float,
        status_voltage: Status,
        status_amperage: Status,
    ) -> None:
        """
        Initialize Phase.

        :param name: phase name
        :type name: str
        :param voltage: phase AC voltage in V
        :type voltage: float
        :param amperage: phase AC amperage in A
        :type amperage: float
        :param status_voltage: phase AC voltage status
        :type status_voltage: Status
        :param status_amperage: phase AC amperage status
        :type status_amperage: Status
        """
        self._name = name
        self._voltage = voltage
        self._amperage = amperage
        self._status_voltage = status_voltage
        self._status_amperage = status_amperage

    @property
    def name(self) -> str:
        """
        Get phase name.

        :return: phase name
        :rtype: str
        """
        return self._name

    @property
    def voltage(self) -> float:
        """
        Get phase AC voltage in V.

        :return: phase AC voltage in V
        :rtype: float
        """
        return self._voltage

    @property
    def amperage(self) -> float:
        """
        Get phase AC amperage in A.

        :return: phase AC amperage in A
        :rtype: float
        """
        return self._amperage

    @property
    def status_voltage(self) -> Status:
        """
        Get phase AC voltage status.

        :return: phase AC voltage status
        :rtype: Status
        """
        return self._status_voltage

    @property
    def status_amperage(self) -> Status:
        """
        Get phase AC amperage status.

        :return: phase AC amperage status
        :rtype: Status
        """
        return self._status_amperage

    def __str__(self) -> str:
        """Cast Phase to str."""
        return str(self.__class__) + ": " + str(self.__dict__)


class String:
    """String details."""

    def __init__(
        self, name: str, voltage: float, amperage: float, status: Status
    ) -> None:
        """
        Initialize String.

        :param name: string name
        :type name: str
        :param voltage: string DC voltage in V
        :type voltage: float
        :param amperage: string DC amperage in A
        :type amperage: float
        :param status: string status
        :type status: Status
        """
        self._name = name
        self._voltage = voltage
        self._amperage = amperage
        self._status = status

    @property
    def name(self) -> str:
        """
        Get string name.

        :return: string name
        :rtype: str
        """
        return self._name

    @property
    def voltage(self) -> float:
        """
        Get string DC voltage in V.

        :return: string DC voltage in V
        :rtype: float
        """
        return self._voltage

    @property
    def amperage(self) -> float:
        """
        Get string DC amperage in A.

        :return: string DC amperage in A
        :rtype: float
        """
        return self._amperage

    @property
    def status(self) -> Status:
        """
        Get string status.

        :return: string status
        :rtype: Status
        """
        return self._status

    def __str__(self) -> str:
        """Cast String to str."""
        return str(self.__class__) + ": " + str(self.__dict__)


class MPPT:
    """MPPT details."""

    def __init__(self, name: str) -> None:
        """
        Initialize MPPT.

        :param name: MPPT name
        :type name: srt
        """
        self._name = name
        self._strings: list[String] = []

    @property
    def name(self) -> str:
        """
        Get MPPT name.

        :return: MPPT name
        :rtype: str
        """
        return self._name

    @property
    def strings(self) -> list[String]:
        """
        Get list of MPPT's String.

        :return: list of Strings
        :rtype: list[String]
        """
        return self._strings

    def __str__(self) -> str:
        """Cast MPPT to str."""
        return str(self.__class__) + ": " + str(self.__dict__)


class Inverter:
    """Inverter device."""

    def __init__(
        self,
        id: int,
        name: str,
        sn: str,
        status: Status,
        temperature: int,
        total_energy: float = 0,
        today_energy: float = 0,
        power_factor: float = 0,
        frequency: float = 0,
        power: float = 0,
    ) -> None:
        """
        Initialize Inverter.

        :param id: inverter id
        :type id: int
        :param name: inverter name
        :type name: str
        :param sn: inverter serial number
        :type sn: str
        :param status: inverter status
        :type status: Status
        :param temperature: inverter temperature
        :type temperature: int
        :param total_energy: total generated energy in kWh
        :type total_energy: float
        :param today_energy: total generated energy today in kWh
        :type today_energy: float
        :param power_factor: inverter power factor
        :type power_factor: float
        :param frequency: inverter output frequency in Hz
        :type frequency: float
        :param power: inverter output power in W
        :type power: float
        """
        self._id = id
        self._name = name
        self._sn = sn
        self._total_energy = total_energy
        self._today_energy = today_energy
        self._power_factor = power_factor
        self._frequency = frequency
        self._power = power
        self._status = status
        self._temperature = temperature
        self._phases: list[Phase] = []
        self._mppts: list[MPPT] = []

    @property
    def id(self) -> int:
        """
        Get inverter id.

        :return: inverter id
        :rtype: int
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Get inverter name.

        :return: inverter name
        :rtype: str
        """
        return self._name

    @property
    def sn(self) -> str:
        """
        Get inverter serial number.

        :return: inverter serial number
        :rtype: str
        """
        return self._sn

    @property
    def status(self) -> Status:
        """
        Get inverter status.

        :return: inverter status
        :rtype: Status
        """
        return self._status

    @property
    def temperature(self) -> int:
        """
        Get inverter temperature.

        :return: inverter temperature
        :rtype: int
        """
        return self._temperature

    @property
    def today_energy(self) -> float:
        """
        Get inverter today generated energy in kWh.

        :return: inverter today generated energy in kWh
        :rtype: float
        """
        return self._today_energy

    @today_energy.setter
    def today_energy(self, value: float) -> None:
        """
        Set inverter today generated energy in kWh.

        :param value: inverter today generated energy in kWh
        :type value: float
        """
        self._today_energy = value

    @property
    def total_energy(self) -> float:
        """
        Get inverter total generated energy in kWh.

        :return: inverter total generated energy in kWh
        :rtype: float
        """
        return self._total_energy

    @total_energy.setter
    def total_energy(self, value: float) -> None:
        """
        Set inverter total generated energy in kWh.

        :param value: inverter total generated energy in kWh
        :type value: float
        """
        self._total_energy = value

    @property
    def power_factor(self) -> float:
        """
        Get inverter power factor.

        :return: inverter power factor
        :rtype: float
        """
        return self._power_factor

    @power_factor.setter
    def power_factor(self, value: float) -> None:
        """
        Set inverter power factor.

        :param value: inverter power factor
        :type value: float
        """
        self._power_factor = value

    @property
    def frequency(self) -> float:
        """
        Get inverter frequency in Hz.

        :return: inverter frequency in HZ
        :rtype: float
        """
        return self._frequency

    @frequency.setter
    def frequency(self, value: float) -> None:
        """
        Set inverter frequency in Hz.

        :param value: inverter frequency in Hz
        :type value: float
        """
        self._frequency = value

    @property
    def power(self) -> float:
        """
        Get inverter output power in W.

        :return: inverter output power in W
        :rtype: float
        """
        return self._power

    @power.setter
    def power(self, value: float) -> None:
        """
        Set inverter output power in W.

        :param value: inverter output power in W
        :type value: float
        """
        self._power = value

    @property
    def is_complete(self) -> bool:
        """
        Is inverter data complete.

        :return: True when inverter data is complete
        :rtype: bool
        """
        return (
            self._today_energy != 0
            or self._total_energy != 0
            or self._power_factor != 0
            or self._frequency != 0
            or self._power != 0
        )

    @property
    def phases(self) -> list[Phase]:
        """
        Get list of inverter's phases.

        :return: list of phases
        :rtype: list[Phase]
        """
        return self._phases

    @property
    def mppts(self) -> list[MPPT]:
        """
        Get list of inverter's MPPTs.

        :return: list of MPPTs
        :rtype: list[MPPT]
        """
        return self._mppts

    def __str__(self) -> str:
        """Cast Inverter to str."""
        return str(self.__class__) + ": " + str(self.__dict__)
