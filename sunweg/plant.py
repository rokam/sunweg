from datetime import datetime

class Plant:
    inverters = []
    
    def __init__(self, id:int, name:str, total_power:float, kwh_per_kwp:float, performance_rate:float, saving:float,
                    today_energy:float, total_energy:float, total_carbon_saving:float, last_update:datetime):
        self.id = id
        self.name = name
        self.total_power = total_power
        self.kwh_per_kwp = kwh_per_kwp
        self.performance_rate = performance_rate
        self.saving = saving
        self.today_energy = today_energy
        self.total_energy = total_energy
        self.total_carbon_saving = total_carbon_saving
        self.last_update = last_update
    
    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)