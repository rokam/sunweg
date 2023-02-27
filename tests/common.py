"""Test sunweg common."""
from datetime import datetime
from sunweg.device import Inverter, MPPT, Phase, String
from sunweg.plant import Plant
from sunweg.util import Status


PLANT_MOCK = Plant(
    id=1,
    name="Plant",
    total_power=29.2,
    kwh_per_kwp=0.1,
    performance_rate=0,
    saving=0,
    today_energy=123.1,
    total_energy=321.1,
    total_carbon_saving=12.1,
    last_update=datetime.now(),
)

INVERTER_MOCK = Inverter(
    id=1,
    name="Inverter",
    sn="1234ABC",
    total_energy=321.1,
    today_energy=123.1,
    power_factor=0.2,
    frequency=60,
    power=29,
    status=Status.OK,
    temperature=70,
)

MPPT_MOCK = MPPT("MPPT")

STRING_MOCK = String(name="String", voltage=523.1, amperage=12.1, status=Status.OK)

PHASE_MOCK = Phase(
    name="Phase",
    voltage=230.1,
    amperage=3.1,
    status_voltage=Status.OK,
    status_amperage=Status.OK,
)
