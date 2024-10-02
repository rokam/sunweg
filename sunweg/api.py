"""API Helper."""

import json
from dateutil import parser
from typing import Any

from requests import Response, session

from .const import (
    SUNWEG_INVERTER_DETAIL_PATH,
    SUNWEG_LOGIN_PATH,
    SUNWEG_MONTH_STATS_PATH,
    SUNWEG_PLANT_DETAIL_PATH,
    SUNWEG_PLANT_LIST_PATH,
    SUNWEG_URL,
)
from .device import MPPT, Inverter, Phase, String
from .plant import Plant
from .util import ProductionStats, Status


class SunWegApiError(RuntimeError):
    """API Error."""

    pass


class LoginError(SunWegApiError):
    """Login Error."""

    pass


def convert_situation_status(situation: int) -> Status:
    """
    Convert situation to status.

    :param situation: situation
    :type situation: int
    :return: equivalent status
    :rtype: Status
    """
    if situation == 0:
        return Status.ERROR
    if situation == 1:
        return Status.OK
    return Status.WARN


def separate_value_metric(
    value_with_metric: str | None, default_metric: str = "", metric_before: bool = False
) -> tuple[float, str]:
    """
    Separate the value from the metric.

    :param value_with_metric: value with metric separated by space
    :type value_with_metric: str | None
    :param default_metric: metric that should be returned if `value_with_metric` is None
    :type default_metric: str
    :param metric_before: true when metric appears before the value
    :type metric_before: bool
    :return: tuple with value and metric
    :rtype: tuple[float, str]
    """
    if value_with_metric is None or len(value_with_metric) == 0:
        return (0.0, default_metric)
    split = value_with_metric.split(" ")
    if metric_before:
        return (
            float(split[0].replace(",", "."))
            if len(split) < 2
            else float(split[1].replace(",", ".")),
            default_metric if len(split) < 2 else split[0],
        )
    return (
        float(split[0].replace(",", ".")),
        default_metric if len(split) < 2 else split[1],
    )


class APIHelper:
    """Class to call sunweg.net api."""

    SERVER_URI = SUNWEG_URL

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
    ) -> None:
        """
        Initialize APIHelper for SunWEG platform.

        :param username: username for authentication
        :param password: password for authentication
        :param token: token for authentication
        :type username: str
        :type password: str
        :type token: str
        """
        self._token = token
        self._username = username
        self._password = password
        self.session = session()

    def set_token(self, token: str) -> None:
        """
        Set token.

        :param token: token for authentication
        :type token: str
        """
        self._token = token

    def _set_username(self, username: str) -> None:
        """
        Set username.

        :param username: username for authentication
        :type username: str
        """
        self._username = username

    username = property(None, _set_username)

    def _set_password(self, password: str) -> None:
        """
        Set password.

        :param password: password for authentication
        :type password: str
        """
        self._password = password

    password = property(None, _set_password)

    def authenticate(self) -> bool:
        """
        Authenticate with provided username and password.

        :return: True on authentication success
        :rtype: bool
        """
        if self._username is None or self._password is None:
            return False

        user_data = json.dumps(
            {"usuario": self._username, "senha": self._password, "rememberMe": True},
            default=lambda o: o.__dict__,
        )

        result = self._post(SUNWEG_LOGIN_PATH, user_data, False)
        if not result["success"]:
            return False
        self._token = result["token"]
        return result["success"]

    def _headers(self):
        """Retrieve headers with authentication token."""
        if self._token is None:
            return {"Content-Type": "application/json"}
        return {"Content-Type": "application/json", "X-Auth-Token-Update": self._token}

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
            plantlist = (
                result["nao_comissionadas"]
                + result["conectadas"]
                + result["falhas"]
                + result["alertas"]
                + result["atendimento"]
            )

            for plant in plantlist:
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

            (today_energy, today_energy_metric) = separate_value_metric(
                result["energiadia"], "kWh"
            )
            total_power = separate_value_metric(result["AcumuladoPotencia"])[0]
            saving = separate_value_metric(result["economia"], metric_before=True)[0]
            plant = Plant(
                id=id,
                name=result["usinas"]["nome"],
                total_power=total_power,
                kwh_per_kwp=float(0),
                performance_rate=float(0),
                saving=saving,
                today_energy=today_energy,
                today_energy_metric=today_energy_metric,
                total_energy=float(result["energiaacumuladanumber"]),
                total_carbon_saving=result["reduz_carbono_total_number"],
                last_update=parser.parse(result["ultimaAtualizacao"])
                if result["ultimaAtualizacao"] is not None
                else None,
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
            (total_energy, total_energy_metric) = separate_value_metric(
                result["energiaacumulada"], "kWh"
            )
            (today_energy, today_energy_metric) = separate_value_metric(
                result["energiadodia"], "kWh"
            )
            (power, power_metric) = separate_value_metric(result["potenciaativa"], "kW")
            inverter = Inverter(
                id=id,
                name=result["inversor"]["nome"],
                sn=result["inversor"]["esn"],
                total_energy=total_energy,
                total_energy_metric=total_energy_metric,
                today_energy=today_energy,
                today_energy_metric=today_energy_metric,
                power_factor=float(result["fatorpotencia"].replace(",", ".")),
                frequency=float(result["frequencia"].replace(",", ".")),
                power=power,
                power_metric=power_metric,
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
            (
                inverter.total_energy,
                inverter.total_energy_metric,
            ) = separate_value_metric(result["energiaacumulada"], "kWh")
            (
                inverter.today_energy,
                inverter.today_energy_metric,
            ) = separate_value_metric(result["energiadodia"], "kWh")
            (inverter.power, inverter.power_metric) = separate_value_metric(
                result["potenciaativa"], "kW"
            )
            inverter.power_factor = float(result["fatorpotencia"].replace(",", "."))
            inverter.frequency = float(result["frequencia"].replace(",", "."))

            self._populate_MPPT(result=result, inverter=inverter)
        except LoginError:
            if retry:
                self.authenticate()
                self.complete_inverter(inverter, False)

    def month_stats_production(
        self,
        year: int,
        month: int,
        plant: Plant,
        inverter: Inverter | None = None,
        retry: bool = True,
    ) -> list[ProductionStats]:
        """
        Retrieve month energy production statistics.

        :param year: statistics year
        :type year: int
        :param month: statistics month
        :type month: int
        :param plant: statistics plant
        :type plant: Plant
        :param inverter: statistics inverter, None for every inverter
        :type inverter: Inverter | None
        :param retry: reauthenticate if token expired and retry
        :type retry: bool
        :return: list of daily energy production statistics
        :rtype: list[ProductionStats]
        """
        return self.month_stats_production_by_id(
            year, month, plant.id, inverter.id if inverter is not None else None, retry
        )

    def month_stats_production_by_id(
        self,
        year: int,
        month: int,
        plant_id: int,
        inverter_id: int | None = None,
        retry: bool = True,
    ) -> list[ProductionStats]:
        """
        Retrieve month energy production statistics.

        :param year: statistics year
        :type year: int
        :param month: statistics month
        :type month: int
        :param plant_id: id of statistics plant
        :type plant_id: int
        :param inverter_id: id of statistics inverter, None for every inverter
        :type inverter_id: int | None
        :param retry: reauthenticate if token expired and retry
        :type retry: bool
        :return: list of daily energy production statistics
        :rtype: list[ProductionStats]
        """
        inverter_str: str = str(inverter_id) if inverter_id is not None else ""
        try:
            result = self._get(
                SUNWEG_MONTH_STATS_PATH
                + f"idusina={plant_id}&idinversor={inverter_str}&date={format(month,'02')}/{year}"
            )
            return [
                ProductionStats(
                    parser.parse(item["tempoatual"]).date(),
                    float(item["energiapordia"]),
                    float(item["prognostico"]),
                )
                for item in result["graficomes"]
            ]
        except LoginError:
            if retry:
                self.authenticate()
                return self.month_stats_production_by_id(
                    year, month, plant_id, inverter_id, False
                )
            return []

    def _populate_MPPT(self, result: dict, inverter: Inverter) -> None:
        """Populate MPPT information inside a inverter."""
        for str_mppt in result["stringmppt"]:
            mppt = MPPT(str_mppt["nomemppt"])

            for str_string in str_mppt["strings"]:
                string = String(
                    str_string["nome"],
                    float(result["inversor"]["leitura"][str_string["variaveltensao"]]),
                    float(
                        result["inversor"]["leitura"][str_string["variavelcorrente"]]
                    ),
                    convert_situation_status(int(str_string["situacao"])),
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

    def _get(self, path: str, launch_exception_on_error: bool = True) -> dict:
        """Do a get request returning a treated response."""
        res = self.session.get(self.SERVER_URI + path, headers=self._headers())
        result = self._treat_response(res, launch_exception_on_error)
        return result

    def _post(
        self, path: str, data: Any | None, launch_exception_on_error: bool = True
    ) -> dict:
        """Do a post request returning a treated response."""
        res = self.session.post(
            self.SERVER_URI + path, data=data, headers=self._headers()
        )
        result = self._treat_response(res, launch_exception_on_error)
        return result

    def _treat_response(
        self, response: Response, launch_exception_on_error: bool = True
    ) -> dict:
        """Treat the response from requests."""
        if response.status_code == 401:
            raise LoginError("Request failed: %s" % response)
        if response.status_code != 200:
            raise SunWegApiError("Request failed: %s" % response)
        result = response.json()
        if launch_exception_on_error and not result["success"]:
            raise SunWegApiError(result["message"])
        return result
