from datetime import datetime
import json
import requests

from sunweg.const import SUNWEG_LOGIN_PATH, SUNWEG_PLANT_DETAIL_PATH, SUNWEG_PLANT_LIST_PATH, SUNWEG_URL
from sunweg.plant import Plant
from sunweg.util import SingletonMeta

class APIHelper(metaclass=SingletonMeta):
    def __init__(self, username:str, password:str) -> None:
        self._token = None
        self._username = username
        self._password = password

    def authenticate(self)->bool:
        userdata = json.dumps({"usuario":self._username,"senha":self._password}, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        response = json.loads(requests.post(SUNWEG_URL+SUNWEG_LOGIN_PATH, userdata).text)
        self._token = response["token"]
        return response["success"]

    def __headers(self):
        return {'X-Auth-Token-Update' : self._token}

    
    def listPlants(self)->list:
        req = requests.get(SUNWEG_URL+SUNWEG_PLANT_LIST_PATH, headers=self.__headers())
        if req.status_code == 401:
            self.authenticate()
            req = requests.get(SUNWEG_URL+SUNWEG_PLANT_LIST_PATH, headers=self.__headers())
        
        if req.status_code != 200:
            return []
        
        response = json.loads(req.text)
        if not response["success"]:
            return []
        
        ret_list = []
        for usina in response["usinas"]:
            ret_list.append(self.plant(usina["id"]))
        return ret_list
    
    def plant(self, id:int)->Plant:
        req = requests.get(SUNWEG_URL+SUNWEG_PLANT_DETAIL_PATH+str(id), headers=self.__headers())
        if req.status_code == 401:
            self.authenticate()
            req = requests.get(SUNWEG_URL+SUNWEG_PLANT_DETAIL_PATH+str(id), headers=self.__headers())
        
        if req.status_code != 200:
            return None
        response = json.loads(req.text)
        if not response["success"]:
            return None
        
        return Plant(id, 
                    response["usinas"]["nome"],  
                    float(str(response["AcumuladoPotencia"]).replace(" kW","").replace(",",".")), 
                    float(str(response["KWHporkWp"]).replace(",",".")), 
                    response["taxaPerformance"], 
                    response["economia"],
                    float(str(response["energiaGeradaHoje"]).replace(" kWh","").replace(",",".")),
                    float(response["energiaacumuladanumber"]),
                    response["reduz_carbono_total_number"],
                    datetime.strptime(response["ultimaAtualizacao"],"%Y-%m-%d %H:%M:%S"))
