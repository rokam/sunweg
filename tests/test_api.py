"""Test sunweg.api."""

from datetime import date, datetime
from os import path
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch
import pytest

from requests import Response

from sunweg.api import (
    APIHelper,
    convert_situation_status,
    SunWegApiError,
    separate_value_metric,
)
from sunweg.device import Inverter, String
from sunweg.util import Status

from .common import INVERTER_MOCK, PLANT_MOCK


class Api_Test(TestCase):
    """APIHelper test case."""

    responses: dict[str, Response] = {}

    def setUp(self) -> None:
        """Set tests up."""
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

    def test_convert_situation_status(self) -> None:
        """Test the conversion from situation to status."""
        status_ok: Status = convert_situation_status(1)
        status_err: Status = convert_situation_status(0)
        status_wrn: Status = convert_situation_status(2)

        assert status_ok == Status.OK
        assert status_err == Status.ERROR
        assert status_wrn == Status.WARN

    def test_separate_value_metric_comma(self) -> None:
        """Test the separation from value and metric of string with comma."""
        (value, metric) = separate_value_metric("0,0")
        assert value == 0
        assert metric == ""
        (value, metric) = separate_value_metric("1,0", "W")
        assert value == 1.0
        assert metric == "W"
        (value, metric) = separate_value_metric("0,2 kW", "W")
        assert value == 0.2
        assert metric == "kW"

    def test_separate_value_metric_dot(self) -> None:
        """Test the separation from value and metric of string with dot."""
        (value, metric) = separate_value_metric("0.0")
        assert value == 0
        assert metric == ""
        (value, metric) = separate_value_metric("1.0", "W")
        assert value == 1.0
        assert metric == "W"
        (value, metric) = separate_value_metric("0.2 kW", "W")
        assert value == 0.2
        assert metric == "kW"

    def test_separate_value_metric_none_int(self) -> None:
        """Test the separation from value and metric of string with dot."""
        (value, metric) = separate_value_metric(None)
        assert value == 0
        assert metric == ""
        (value, metric) = separate_value_metric("1", "W")
        assert value == 1.0
        assert metric == "W"
        (value, metric) = separate_value_metric("2 kW", "W")
        assert value == 2.0
        assert metric == "kW"

    def test_error500(self) -> None:
        """Test error 500."""
        with patch(
            "requests.Session.post",
            return_value=self.responses["error_500_response.txt"],
        ):
            api = APIHelper("user@acme.com", "password")
            with pytest.raises(SunWegApiError) as e_info:
                api.authenticate()
            assert e_info.value.__str__() == "Request failed: <Response [500]>"

    def test_initialize_token(self) -> None:
        """Test initialize token."""
        api = APIHelper(token="token")
        assert api._token == "token"

    def test_set_token(self) -> None:
        """Test set token."""
        api = APIHelper(token="token")
        api.set_token("new_token")
        assert api._token == "new_token"

    def test_authenticate_success(self) -> None:
        """Test authentication success."""
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_success_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            assert api.authenticate()

    def test_authenticate_fail_empty_credentials(self) -> None:
        """Test authentication failed."""
        api = APIHelper(None, None)
        assert not api.authenticate()

    def test_authenticate_failed(self) -> None:
        """Test authentication failed."""
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_fail_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            assert not api.authenticate()

    def test_list_plants_none_success(self) -> None:
        """Test list plants with empty plant list."""
        with patch(
            "requests.Session.get",
            return_value=self.responses["list_plant_success_none_response.json"],
        ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
            api = APIHelper("user@acme.com", "password")
            assert len(api.listPlants()) == 0

    def test_list_plants_1_success(self) -> None:
        """Test list plants with one plant in the list."""
        with patch(
            "requests.Session.get",
            return_value=self.responses["list_plant_success_1_response.json"],
        ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
            api = APIHelper("user@acme.com", "password")
            assert len(api.listPlants()) == 1

    def test_list_plants_2_success(self) -> None:
        """Test list plants with two plant in the list."""
        with patch(
            "requests.Session.get",
            return_value=self.responses["list_plant_success_2_response.json"],
        ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
            api = APIHelper("user@acme.com", "password")
            assert len(api.listPlants()) == 2

    def test_list_plants_401(self) -> None:
        """Test list plants with expired token."""
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
        """Test plant success."""
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
            assert plant.kwh_per_kwp == 0.0
            assert plant.performance_rate == 0.0
            assert plant.saving == 12.78
            assert plant.today_energy == 1.23
            assert plant.today_energy_metric == "kWh"
            assert plant.total_carbon_saving == 0.012296
            assert plant.total_energy == 23.2
            assert plant.__str__().startswith("<class 'sunweg.plant.Plant'>")
            assert len(plant.inverters) == 1
            for inverter in plant.inverters:
                assert inverter.id == 21255
                assert inverter.name == "Inverter Name"
                assert inverter.frequency == 0
                assert inverter.power == 0.0
                assert inverter.power_metric == ""
                assert inverter.power_factor == 0.0
                assert inverter.sn == "1234ABC"
                assert inverter.status == Status.ERROR
                assert inverter.temperature == 80
                assert inverter.today_energy == 0.0
                assert inverter.today_energy_metric == ""
                assert inverter.total_energy == 0.0
                assert inverter.total_energy_metric == ""
                assert not inverter.is_complete

    def test_plant_success_alt(self) -> None:
        """Test plant success."""
        with patch(
            "requests.Session.get",
            return_value=self.responses["plant_success_alt_response.json"],
        ), patch("sunweg.api.APIHelper.inverter", return_value=INVERTER_MOCK):
            api = APIHelper("user@acme.com", "password")
            plant = api.plant(16925)
            assert plant is not None
            assert plant.id == 16925
            assert plant.name == "Plant Name"
            assert plant.total_power == 25.23
            assert plant.last_update is None
            assert plant.kwh_per_kwp == 0.0
            assert plant.performance_rate == 0.0
            assert plant.saving == 12.78
            assert plant.today_energy == 1.23
            assert plant.today_energy_metric == "kWh"
            assert plant.total_carbon_saving == 0.012296
            assert plant.total_energy == 23.2
            assert plant.__str__().startswith("<class 'sunweg.plant.Plant'>")
            assert len(plant.inverters) == 1
            for inverter in plant.inverters:
                assert inverter.id == 21255
                assert inverter.name == "Inverter Name"
                assert inverter.frequency == 0
                assert inverter.power == 0.0
                assert inverter.power_metric == ""
                assert inverter.power_factor == 0.0
                assert inverter.sn == "1234ABC"
                assert inverter.status == Status.ERROR
                assert inverter.temperature == 80
                assert inverter.today_energy == 0.0
                assert inverter.today_energy_metric == ""
                assert inverter.total_energy == 0.0
                assert inverter.total_energy_metric == ""
                assert not inverter.is_complete

    def test_plant_401(self) -> None:
        """Test plant with expired token."""
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
        """Test inverter success."""
        with patch(
            "requests.Session.get",
            return_value=self.responses["inverter_success_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            inverter = api.inverter(21255)
            assert inverter is not None
            assert inverter.id == 21255
            assert inverter.name == "Inverter Name"
            assert inverter.frequency == 59.85
            assert inverter.power == 0.0
            assert inverter.power_metric == "kW"
            assert inverter.power_factor == 0.0
            assert inverter.sn == "1234ABC"
            assert inverter.status == Status.OK
            assert inverter.temperature == 80
            assert inverter.today_energy == 0.0
            assert inverter.today_energy_metric == "kWh"
            assert inverter.total_energy == 23.2
            assert inverter.today_energy_metric == "kWh"
            strings: list[String] = []
            for mppt in inverter.mppts:
                assert mppt.__str__().startswith("<class 'sunweg.device.MPPT'>")
                assert mppt.name != ""
                strings.extend(mppt.strings)
            assert len(strings) == 4
            assert len(inverter.phases) == 3
            assert inverter.__str__().startswith("<class 'sunweg.device.Inverter'>")
            for string in strings:
                assert string.name != ""
                assert string.amperage != 0
                assert string.voltage != 0
                assert string.status == Status.OK
                assert string.__str__().startswith("<class 'sunweg.device.String'>")
            for phase in inverter.phases:
                assert phase.name != ""
                assert phase.amperage != 0
                assert phase.voltage != 0
                assert phase.status_amperage == Status.OK
                assert phase.status_voltage == Status.ERROR
                assert phase.__str__().startswith("<class 'sunweg.device.Phase'>")

    def test_inverter_401(self) -> None:
        """Test inverter with expired token."""
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_success_response.json"],
        ), patch(
            "requests.Session.get",
            return_value=self.responses["error_401_response.txt"],
        ):
            api = APIHelper("user@acme.com", "password")
            assert api.inverter(21255) is None

    def test_complete_inverter_success(self) -> None:
        """Test complete inverter success."""
        with patch(
            "requests.Session.get",
            return_value=self.responses["inverter_success_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            inverter = Inverter(
                id=12345,
                name="Other inverter name",
                sn="1234ABCD",
                status=Status.ERROR,
                temperature=70,
            )
            api.complete_inverter(inverter)
            assert inverter is not None
            assert inverter.id == 12345
            assert inverter.name == "Other inverter name"
            assert inverter.frequency == 59.85
            assert inverter.power == 0.0
            assert inverter.power_factor == 0.0
            assert inverter.sn == "1234ABCD"
            assert inverter.status == Status.ERROR
            assert inverter.temperature == 70
            assert inverter.today_energy == 0.0
            assert inverter.total_energy == 23.2
            strings: list[String] = []
            for mppt in inverter.mppts:
                assert mppt.__str__().startswith("<class 'sunweg.device.MPPT'>")
                assert mppt.name != ""
                strings.extend(mppt.strings)
            assert len(strings) == 4
            assert len(inverter.phases) == 3
            assert inverter.__str__().startswith("<class 'sunweg.device.Inverter'>")
            for string in strings:
                assert string.name != ""
                assert string.amperage != 0
                assert string.voltage != 0
                assert string.status == Status.OK
                assert string.__str__().startswith("<class 'sunweg.device.String'>")
            for phase in inverter.phases:
                assert phase.name != ""
                assert phase.amperage != 0
                assert phase.voltage != 0
                assert phase.status_amperage == Status.OK
                assert phase.status_voltage == Status.ERROR
                assert phase.__str__().startswith("<class 'sunweg.device.Phase'>")

    def test_complete_inverter_401(self) -> None:
        """Test complete inverter with expired token."""
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_success_response.json"],
        ), patch(
            "requests.Session.get",
            return_value=self.responses["error_401_response.txt"],
        ):
            api = APIHelper("user@acme.com", "password")
            inverter = Inverter(
                id=12345,
                name="Other inverter name",
                sn="1234ABCD",
                status=Status.ERROR,
                temperature=70,
            )
            api.complete_inverter(inverter)
            assert not inverter.is_complete

    def test_setters(self) -> None:
        """Test API setters."""
        api = APIHelper("user@acme.com", "password")
        assert api._username == "user@acme.com"
        assert api._password == "password"
        api.username = "user1@acme.com"
        api.password = "password1"
        assert api._username == "user1@acme.com"
        assert api._password == "password1"

    def test_month_stats_fail(self) -> None:
        """Test month stats with error from server."""
        with patch(
            "requests.Session.get",
            return_value=self.responses["month_stats_fail_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            plant = MagicMock()
            plant.id = 1
            with pytest.raises(SunWegApiError) as e_info:
                api.month_stats_production(2013, 12, plant)
            assert e_info.value.__str__() == "Error message"

    def test_month_stats_401(self) -> None:
        """Test month stats with data from server with expired token."""
        with patch(
            "requests.Session.post",
            return_value=self.responses["auth_success_response.json"],
        ), patch(
            "requests.Session.get",
            return_value=self.responses["error_401_response.txt"],
        ):
            api = APIHelper("user@acme.com", "password")
            plant = MagicMock()
            plant.id = 1
            stats = api.month_stats_production(2023, 12, plant)
            assert isinstance(stats, list)
            assert len(stats) == 0

    def test_month_stats_success(self) -> None:
        """Test month stats with data from server."""
        with patch(
            "requests.Session.get",
            return_value=self.responses["month_stats_success_response.json"],
        ):
            api = APIHelper("user@acme.com", "password")
            plant = MagicMock()
            plant.id = 1
            stats = api.month_stats_production(2023, 12, plant)
            assert len(stats) > 0
            i: int = 1
            for stat in stats:
                assert stat.date == date(2024, 5, i)
                assert isinstance(stat.production, float)
                assert stat.prognostic == 111.03225806451613
                assert stat.__str__().startswith(
                    "<class 'sunweg.util.ProductionStats'>"
                )
                i += 1
