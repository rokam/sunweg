from sunweg.util import Status

class Inverter:
    
    def __init__(self, id:int, total_energy:float, today_energy:float, power_factor:float, frequency:float,
                 power:float, status:Status, temperature:int) -> None:
        self._id = id
        self._total_energy = total_energy
        self._today_energy = today_energy
        self._power_factor = power_factor
        self._frequency = frequency
        self._power = power
        self._status = status
        self._temperature = temperature
        self.phases = []
        self.mppts = []
    
    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)

class Phase:
    def __init__(self, name:str, voltage:float, current:float, status_voltage:Status, status_current:Status) -> None:
        self._name = name
        self._voltage = voltage
        self._current = current
        self._status_voltage = status_voltage
        self._status_current = status_current
    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)

class MPPT:
    def __init__(self, name:str) -> None:
        self._name = name
        self.strings = []

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)

class String:
    def __init__(self, name:str, voltage:float, current:float, status:Status) -> None:
        self._name = name
        self._voltage = voltage
        self._current = current
        self._status = status
    
    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)