import json
from datetime import datetime
from typing import Any

from requests import Response, session

from .const import (
    SUNWEG_INVERTER_DETAIL_PATH,
    SUNWEG_LOGIN_PATH,
    SUNWEG_PLANT_DETAIL_PATH,
    SUNWEG_PLANT_LIST_PATH,
    SUNWEG_URL,
)
from .device import MPPT, Inverter, Phase, String
from .plant import Plant
from .util import SingletonMeta, Status


class SunWegApiError(RuntimeError):
    pass


class LoginError(SunWegApiError):
    pass


class APIHelper(metaclass=SingletonMeta):
    SERVER_URI = SUNWEG_URL

    def __init__(self, username: str, password: str) -> None:
        self._token = None
        self._username = username
        self._password = password
        self.session = session()

    def authenticate(self) -> bool:
        userdata = json.dumps(
            {"usuario": self._username, "senha": self._password},
            default=lambda o: o.__dict__,
        )

        result = self._post(SUNWEG_LOGIN_PATH, userdata)
        self._token = result["token"]
        return result["success"]

    def _headers(self):
        if self._token is None:
            return {}
        return {"X-Auth-Token-Update": self._token}

    def listPlants(self, retry=True) -> list[Plant]:
        try:
            result = self._get(SUNWEG_PLANT_LIST_PATH)
            ret_list = []
            for usina in result["usinas"]:
                if (plant := self.plant(usina["id"])) is not None:
                    ret_list.append(plant)
            return ret_list
        except LoginError:
            if retry:
                self.authenticate()
                return self.listPlants(False)
            return []

    def plant(self, id: int, retry=True) -> Plant | None:
        try:
            result = self._get(SUNWEG_PLANT_DETAIL_PATH + str(id))

            plant = Plant(
                id,
                result["usinas"]["nome"],
                float(
                    str(result["AcumuladoPotencia"])
                    .replace(" kW", "")
                    .replace(",", ".")
                ),
                float(str(result["KWHporkWp"]).replace(",", "."))
                if result["KWHporkWp"] != ""
                else float(0),
                result["taxaPerformance"],
                result["economia"],
                float(
                    str(result["energiaGeradaHoje"])
                    .replace(" kWh", "")
                    .replace(",", ".")
                ),
                float(result["energiaacumuladanumber"]),
                result["reduz_carbono_total_number"],
                datetime.strptime(result["ultimaAtualizacao"], "%Y-%m-%d %H:%M:%S"),
            )

            for inv in result["usinas"]["inversores"]:
                if (inverter := self.inverter(inv["id"])) is not None:
                    plant.inverters.append(inverter)

            return plant
        except LoginError:
            if retry:
                self.authenticate()
                return self.plant(id, False)
            return None

    def inverter(self, id: int, retry=True) -> Inverter | None:
        try:
            result = self._get(SUNWEG_INVERTER_DETAIL_PATH + str(id))
            inverter = Inverter(
                id,
                result["inversor"]["descricao"],
                result["inversor"]["esn"],
                float(result["energiaAcumulada"].replace(" kWh", "").replace(",", ".")),
                float(result["energiaDoDia"].replace(" kWh", "").replace(",", ".")),
                float(result["fatorpotencia"].replace(",", ".")),
                result["frequencia"],
                float(result["potenciaativa"].replace(" kW", "").replace(",", ".")),
                Status(int(result["statusInversor"])),
                result["temperatura"],
            )

            for strmppt in result["stringmppt"]:
                mppt = MPPT(strmppt["nomemppt"])

                for strstring in strmppt["strings"]:
                    string = String(
                        strstring["nome"],
                        float(strstring["valorTensao"]),
                        float(strstring["valorCorrente"]),
                        Status(int(strstring["status"])),
                    )
                    mppt.strings.append(string)

                inverter.mppts.append(mppt)

            for phasename in result["correnteCA"].keys():
                if str(phasename).endswith("status"):
                    continue
                inverter.phases.append(
                    Phase(
                        phasename,
                        float(result["tensaoca"][phasename].replace(",", ".")),
                        float(result["correnteCA"][phasename].replace(",", ".")),
                        Status(result["tensaoca"][phasename + "status"]),
                        Status(result["correnteCA"][phasename + "status"]),
                    )
                )

            return inverter
        except LoginError:
            if retry:
                self.authenticate()
                return self.inverter(id, False)
            return None

    def _get(self, path: str) -> dict:
        res = self.session.get(self.SERVER_URI + path, headers=self._headers())
        result = self._treat_response(res)
        return result

    def _post(self, path: str, data: Any | None) -> dict:
        res = self.session.post(
            self.SERVER_URI + path, data=data, headers=self._headers()
        )
        result = self._treat_response(res)
        return result

    def _treat_response(self, response: Response) -> dict:
        if response.status_code == 401:
            raise LoginError("Request failed: %s" % response)
        if response.status_code != 200:
            raise SunWegApiError("Request failed: %s" % response)
        result = response.json()
        if not result["success"]:
            raise SunWegApiError(result["message"])
        return result
