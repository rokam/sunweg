"""API Helper."""
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
    """API Error."""

    pass


class LoginError(SunWegApiError):
    """Login Error."""

    pass


class APIHelper(metaclass=SingletonMeta):
    """Singleton class to call sunweg.net api."""

    SERVER_URI = SUNWEG_URL

    def __init__(self, username: str, password: str) -> None:
        """
        Initialize APIHelper for SunWEG platform.

        :param username: username for authentication
        :param password: password for authentication
        :type username: str
        :type password: str
        """
        self._token = None
        self._username = username
        self._password = password
        self.session = session()

    def authenticate(self) -> bool:
        """
        Authenticate with provided username and password.

        :return: True on authentication success
        :rtype: bool
        """
        user_data = json.dumps(
            {"usuario": self._username, "senha": self._password},
            default=lambda o: o.__dict__,
        )

        result = self._post(SUNWEG_LOGIN_PATH, user_data)
        self._token = result["token"]
        return result["success"]

    def _headers(self):
        """Retrieve headers with authentication token."""
        if self._token is None:
            return {}
        return {"X-Auth-Token-Update": self._token}

    def listPlants(self, retry=True) -> list[Plant]:
        """
        Retrieve the list of plants with incomplete inverter information.

        You may want to call `complete_inverter()` to complete the Inverter information.

        :param retry: reauthenticate if token expired and retry
        :type retry: bool
        :return: list of Plant
        :rtype: list[Plant]
        """
        try:
            result = self._get(SUNWEG_PLANT_LIST_PATH)
            ret_list = []
            for plant in result["usinas"]:
                if (plant := self.plant(plant["id"])) is not None:
                    ret_list.append(plant)
            return ret_list
        except LoginError:
            if retry:
                self.authenticate()
                return self.listPlants(False)
            return []

    def plant(self, id: int, retry=True) -> Plant | None:
        """
        Retrieve plant detail by plant id.

        :param id: plant id
        :type id: int
        :param retry: reauthenticate if token expired and retry
        :type retry: bool
        :return: Plant or None if `id` not found.
        :rtype: Plant | None
        """
        try:
            result = self._get(SUNWEG_PLANT_DETAIL_PATH + str(id))

            plant = Plant(
                id=id,
                name=result["usinas"]["nome"],
                total_power=float(
                    str(result["AcumuladoPotencia"])
                    .replace(" kW", "")
                    .replace(",", ".")
                ),
                kwh_per_kwp=float(str(result["KWHporkWp"]).replace(",", "."))
                if result["KWHporkWp"] != ""
                else float(0),
                performance_rate=result["taxaPerformance"],
                saving=result["economia"],
                today_energy=float(
                    str(result["energiaGeradaHoje"])
                    .replace(" kWh", "")
                    .replace(",", ".")
                ),
                total_energy=float(result["energiaacumuladanumber"]),
                total_carbon_saving=result["reduz_carbono_total_number"],
                last_update=datetime.strptime(
                    result["ultimaAtualizacao"], "%Y-%m-%d %H:%M:%S"
                ),
            )

            plant.inverters.extend(
                [
                    Inverter(
                        id=inv["id"],
                        name=inv["nome"],
                        sn=inv["esn"],
                        status=Status(int(inv["situacao"])),
                        temperature=inv["temperatura"],
                    )
                    for inv in result["usinas"]["inversores"]
                ]
            )
            return plant
        except LoginError:
            if retry:
                self.authenticate()
                return self.plant(id, False)
            return None

    def inverter(self, id: int, retry=True) -> Inverter | None:
        """
        Retrieve inverter detail by inverter id.

        :param id: inverter id
        :type id: int
        :param retry: reauthenticate if token expired and retry
        :type retry: bool
        :return: Inverter or None if `id` not found.
        :rtype: Inverter | None
        """
        try:
            result = self._get(SUNWEG_INVERTER_DETAIL_PATH + str(id))
            inverter = Inverter(
                id=id,
                name=result["inversor"]["nome"],
                sn=result["inversor"]["esn"],
                total_energy=float(
                    result["energiaAcumulada"].replace(" kWh", "").replace(",", ".")
                ),
                today_energy=float(
                    result["energiaDoDia"].replace(" kWh", "").replace(",", ".")
                ),
                power_factor=float(result["fatorpotencia"].replace(",", ".")),
                frequency=result["frequencia"],
                power=float(
                    result["potenciaativa"].replace(" kW", "").replace(",", ".")
                ),
                status=Status(int(result["statusInversor"])),
                temperature=result["temperatura"],
            )

            self._populate_MPPT(result=result, inverter=inverter)

            return inverter
        except LoginError:
            if retry:
                self.authenticate()
                return self.inverter(id, False)
            return None

    def complete_inverter(self, inverter: Inverter, retry=True) -> None:
        """
        Complete inverter data.

        :param inverter: inverter object to be completed with information
        :type inverter: Inverter
        :param retry: reauthenticate if token expired and retry
        :type retry: bool
        """
        try:
            result = self._get(SUNWEG_INVERTER_DETAIL_PATH + str(inverter.id))
            inverter.total_energy = float(
                result["energiaAcumulada"].replace(" kWh", "").replace(",", ".")
            )
            inverter.today_energy = float(
                result["energiaDoDia"].replace(" kWh", "").replace(",", ".")
            )
            inverter.power_factor = float(result["fatorpotencia"].replace(",", "."))
            inverter.frequency = result["frequencia"]
            inverter.power = float(
                result["potenciaativa"].replace(" kW", "").replace(",", ".")
            )

            self._populate_MPPT(result=result, inverter=inverter)
        except LoginError:
            if retry:
                self.authenticate()
                self.complete_inverter(inverter, False)

    def _populate_MPPT(self, result: dict, inverter: Inverter) -> None:
        """Populate MPPT information inside a inverter."""
        for str_mppt in result["stringmppt"]:
            mppt = MPPT(str_mppt["nomemppt"])

            for str_string in str_mppt["strings"]:
                string = String(
                    str_string["nome"],
                    float(str_string["valorTensao"]),
                    float(str_string["valorCorrente"]),
                    Status(int(str_string["status"])),
                )
                mppt.strings.append(string)

            inverter.mppts.append(mppt)

        for phase_name in result["correnteCA"].keys():
            if str(phase_name).endswith("status"):
                continue
            inverter.phases.append(
                Phase(
                    phase_name,
                    float(result["tensaoca"][phase_name].replace(",", ".")),
                    float(result["correnteCA"][phase_name].replace(",", ".")),
                    Status(result["tensaoca"][phase_name + "status"]),
                    Status(result["correnteCA"][phase_name + "status"]),
                )
            )

    def _get(self, path: str) -> dict:
        """Do a get request returning a treated response."""
        res = self.session.get(self.SERVER_URI + path, headers=self._headers())
        result = self._treat_response(res)
        return result

    def _post(self, path: str, data: Any | None) -> dict:
        """Do a post request returning a treated response."""
        res = self.session.post(
            self.SERVER_URI + path, data=data, headers=self._headers()
        )
        result = self._treat_response(res)
        return result

    def _treat_response(self, response: Response) -> dict:
        """Treat the response from requests."""
        if response.status_code == 401:
            raise LoginError("Request failed: %s" % response)
        if response.status_code != 200:
            raise SunWegApiError("Request failed: %s" % response)
        result = response.json()
        if not result["success"]:
            raise SunWegApiError(result["message"])
        return result
