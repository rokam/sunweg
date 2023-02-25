from datetime import datetime
from os import path
import os
from unittest import TestCase
from unittest.mock import patch
import pytest

from requests import Response

from sunweg.api import APIHelper, SunWegApiError
from sunweg.util import Status

from .common import INVERTER_MOCK, PLANT_MOCK


class Api_Test(TestCase):
    responses: dict[str, Response] = {}

    def setUp(self) -> None:
        for file in os.listdir(path.join(path.dirname(__file__), "responses")):
            filename = path.basename(file)
            with open(path.join(path.dirname(__file__), "responses", file)) as f:
                response = Response()
                if filename.startswith("error"):
                    response.status_code = int(filename.split("_")[1])
                    response.reason = "".join(f.readlines())
                else:
                    response.status_code = 200
                    response._content = "".join(f.readlines()).encode()
                self.responses[filename] = response

    def test_error500(self) -> None:
        with patch(
            "requests.Session.post",
            return_value=self.responses["error_500_response.txt"],
        ):
            api = APIHelper("user@acme.com", "password")
            with pytest.raises(SunWegApiError) as e_info:
                api.authenticate()
            assert e_info.value.__str__() == "Request failed: <Response [500]>"

    def test_authenticate_success(self) -> None:
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_success_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            assert api.authenticate()

    def test_authenticate_failed(self) -> None:
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_fail_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            with pytest.raises(SunWegApiError) as e_info:
                api.authenticate()
            assert e_info.value.__str__() == "Error message"

    def test_list_plants_none_success(self) -> None:
        with patch(
            "requests.Session.get",
            return_value=self.responses["list_plant_success_none_response.json"],
        ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
            api = APIHelper("user@acme.com", "password")
            assert len(api.listPlants()) == 0

    def test_list_plants_1_success(self) -> None:
        with patch(
            "requests.Session.get",
            return_value=self.responses["list_plant_success_1_response.json"],
        ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
            api = APIHelper("user@acme.com", "password")
            assert len(api.listPlants()) == 1

    def test_list_plants_2_success(self) -> None:
        with patch(
            "requests.Session.get",
            return_value=self.responses["list_plant_success_2_response.json"],
        ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
            api = APIHelper("user@acme.com", "password")
            assert len(api.listPlants()) == 2

    def test_list_plants_401(self) -> None:
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_success_response.json"],
        ), patch(
            "requests.Session.get",
            return_value=self.responses["error_401_response.txt"],
        ):
            api = APIHelper("user@acme.com", "password")
            assert len(api.listPlants()) == 0

    def test_plant_success(self) -> None:
        with patch(
            "requests.Session.get",
            return_value=self.responses["plant_success_response.json"],
        ), patch("sunweg.api.APIHelper.inverter", return_value=INVERTER_MOCK):
            api = APIHelper("user@acme.com", "password")
            plant = api.plant(16925)
            assert plant is not None
            assert plant.id == 16925
            assert plant.name == "Plant Name"
            assert plant.total_power == 25.23
            assert plant.last_update == datetime(2023, 2, 25, 8, 4, 22)
            assert plant.kwh_per_kwp == 1.2
            assert plant.performance_rate == 1.48
            assert plant.saving == 12.786912
            assert plant.today_energy == 1.23
            assert plant.total_carbon_saving == 0.012296
            assert plant.total_energy == 23.2
            assert plant.__str__().startswith("<class 'sunweg.plant.Plant'>")
            assert len(plant.inverters) == 1

    def test_plant_401(self) -> None:
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_success_response.json"],
        ), patch(
            "requests.Session.get",
            return_value=self.responses["error_401_response.txt"],
        ):
            api = APIHelper("user@acme.com", "password")
            assert api.plant(16925) is None

    def test_inverter_success(self) -> None:
        with patch(
            "requests.Session.get",
            return_value=self.responses["inverter_success_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            inverter = api.inverter(21255)
            assert inverter is not None
            assert inverter.id == 21255
            assert inverter.name == "Inverter Description"
            assert inverter.frequency == 0
            assert inverter.power == 0.0
            assert inverter.power_factor == 0.0
            assert inverter.sn == "1234ABC"
            assert inverter.status == Status.OK
            assert inverter.temperature == 0
            assert inverter.today_energy == 0.0
            assert inverter.total_energy == 23.2
            strings = []
            for mppt in inverter.mppts:
                assert mppt.__str__().startswith("<class 'sunweg.device.MPPT'>")
                strings.extend(mppt.strings)
            assert len(strings) == 4
            assert len(inverter.phases) == 3
            assert inverter.__str__().startswith("<class 'sunweg.device.Inverter'>")
            for string in strings:
                assert string.__str__().startswith("<class 'sunweg.device.String'>")
            for phase in inverter.phases:
                assert phase.__str__().startswith("<class 'sunweg.device.Phase'>")

    def test_inverter_401(self) -> None:
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_success_response.json"],
        ), patch(
            "requests.Session.get",
            return_value=self.responses["error_401_response.txt"],
        ):
            api = APIHelper("user@acme.com", "password")
            assert api.inverter(21255) is None
