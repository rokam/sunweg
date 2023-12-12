# Table of Contents

* [sunweg](#sunweg)
* [sunweg.const](#sunweg.const)
  * [SUNWEG\_URL](#sunweg.const.SUNWEG_URL)
  * [SUNWEG\_LOGIN\_PATH](#sunweg.const.SUNWEG_LOGIN_PATH)
  * [SUNWEG\_PLANT\_LIST\_PATH](#sunweg.const.SUNWEG_PLANT_LIST_PATH)
  * [SUNWEG\_PLANT\_DETAIL\_PATH](#sunweg.const.SUNWEG_PLANT_DETAIL_PATH)
  * [SUNWEG\_INVERTER\_DETAIL\_PATH](#sunweg.const.SUNWEG_INVERTER_DETAIL_PATH)
* [sunweg.device](#sunweg.device)
  * [Phase](#sunweg.device.Phase)
    * [\_\_init\_\_](#sunweg.device.Phase.__init__)
    * [name](#sunweg.device.Phase.name)
    * [voltage](#sunweg.device.Phase.voltage)
    * [amperage](#sunweg.device.Phase.amperage)
    * [status\_voltage](#sunweg.device.Phase.status_voltage)
    * [status\_amperage](#sunweg.device.Phase.status_amperage)
    * [\_\_str\_\_](#sunweg.device.Phase.__str__)
  * [String](#sunweg.device.String)
    * [\_\_init\_\_](#sunweg.device.String.__init__)
    * [name](#sunweg.device.String.name)
    * [voltage](#sunweg.device.String.voltage)
    * [amperage](#sunweg.device.String.amperage)
    * [status](#sunweg.device.String.status)
    * [\_\_str\_\_](#sunweg.device.String.__str__)
  * [MPPT](#sunweg.device.MPPT)
    * [\_\_init\_\_](#sunweg.device.MPPT.__init__)
    * [name](#sunweg.device.MPPT.name)
    * [strings](#sunweg.device.MPPT.strings)
    * [\_\_str\_\_](#sunweg.device.MPPT.__str__)
  * [Inverter](#sunweg.device.Inverter)
    * [\_\_init\_\_](#sunweg.device.Inverter.__init__)
    * [id](#sunweg.device.Inverter.id)
    * [name](#sunweg.device.Inverter.name)
    * [sn](#sunweg.device.Inverter.sn)
    * [status](#sunweg.device.Inverter.status)
    * [temperature](#sunweg.device.Inverter.temperature)
    * [today\_energy](#sunweg.device.Inverter.today_energy)
    * [today\_energy](#sunweg.device.Inverter.today_energy)
    * [today\_energy\_metric](#sunweg.device.Inverter.today_energy_metric)
    * [today\_energy\_metric](#sunweg.device.Inverter.today_energy_metric)
    * [total\_energy](#sunweg.device.Inverter.total_energy)
    * [total\_energy](#sunweg.device.Inverter.total_energy)
    * [total\_energy\_metric](#sunweg.device.Inverter.total_energy_metric)
    * [total\_energy\_metric](#sunweg.device.Inverter.total_energy_metric)
    * [power\_factor](#sunweg.device.Inverter.power_factor)
    * [power\_factor](#sunweg.device.Inverter.power_factor)
    * [frequency](#sunweg.device.Inverter.frequency)
    * [frequency](#sunweg.device.Inverter.frequency)
    * [power](#sunweg.device.Inverter.power)
    * [power](#sunweg.device.Inverter.power)
    * [power\_metric](#sunweg.device.Inverter.power_metric)
    * [power\_metric](#sunweg.device.Inverter.power_metric)
    * [is\_complete](#sunweg.device.Inverter.is_complete)
    * [phases](#sunweg.device.Inverter.phases)
    * [mppts](#sunweg.device.Inverter.mppts)
    * [\_\_str\_\_](#sunweg.device.Inverter.__str__)
* [sunweg.plant](#sunweg.plant)
  * [Plant](#sunweg.plant.Plant)
    * [\_\_init\_\_](#sunweg.plant.Plant.__init__)
    * [id](#sunweg.plant.Plant.id)
    * [name](#sunweg.plant.Plant.name)
    * [total\_power](#sunweg.plant.Plant.total_power)
    * [kwh\_per\_kwp](#sunweg.plant.Plant.kwh_per_kwp)
    * [performance\_rate](#sunweg.plant.Plant.performance_rate)
    * [saving](#sunweg.plant.Plant.saving)
    * [today\_energy](#sunweg.plant.Plant.today_energy)
    * [today\_energy\_metric](#sunweg.plant.Plant.today_energy_metric)
    * [total\_energy](#sunweg.plant.Plant.total_energy)
    * [total\_carbon\_saving](#sunweg.plant.Plant.total_carbon_saving)
    * [last\_update](#sunweg.plant.Plant.last_update)
    * [inverters](#sunweg.plant.Plant.inverters)
    * [\_\_str\_\_](#sunweg.plant.Plant.__str__)
* [sunweg.api](#sunweg.api)
  * [SunWegApiError](#sunweg.api.SunWegApiError)
  * [LoginError](#sunweg.api.LoginError)
  * [APIHelper](#sunweg.api.APIHelper)
    * [\_\_init\_\_](#sunweg.api.APIHelper.__init__)
    * [authenticate](#sunweg.api.APIHelper.authenticate)
    * [listPlants](#sunweg.api.APIHelper.listPlants)
    * [plant](#sunweg.api.APIHelper.plant)
    * [inverter](#sunweg.api.APIHelper.inverter)
    * [complete\_inverter](#sunweg.api.APIHelper.complete_inverter)
* [sunweg.util](#sunweg.util)
  * [Status](#sunweg.util.Status)

<a id="sunweg"></a>

# sunweg

Sunweg API library.

<a id="sunweg.const"></a>

# sunweg.const

Sunweg API constants.

<a id="sunweg.const.SUNWEG_URL"></a>

#### SUNWEG\_URL

SunWEG API URL

<a id="sunweg.const.SUNWEG_LOGIN_PATH"></a>

#### SUNWEG\_LOGIN\_PATH

SunWEG API login path

<a id="sunweg.const.SUNWEG_PLANT_LIST_PATH"></a>

#### SUNWEG\_PLANT\_LIST\_PATH

SunWEG API list plants path

<a id="sunweg.const.SUNWEG_PLANT_DETAIL_PATH"></a>

#### SUNWEG\_PLANT\_DETAIL\_PATH

SunWEG API plant details path

<a id="sunweg.const.SUNWEG_INVERTER_DETAIL_PATH"></a>

#### SUNWEG\_INVERTER\_DETAIL\_PATH

SunWEG API inverter details path

<a id="sunweg.device"></a>

# sunweg.device

Sunweg API devices.

<a id="sunweg.device.Phase"></a>

## Phase Objects

```python
class Phase()
```

Phase details.

<a id="sunweg.device.Phase.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, voltage: float, amperage: float,
             status_voltage: Status, status_amperage: Status) -> None
```

Initialize Phase.

**Arguments**:

- `name` (`str`): phase name
- `voltage` (`float`): phase AC voltage in V
- `amperage` (`float`): phase AC amperage in A
- `status_voltage` (`Status`): phase AC voltage status
- `status_amperage` (`Status`): phase AC amperage status

<a id="sunweg.device.Phase.name"></a>

#### name

```python
@property
def name() -> str
```

Get phase name.

**Returns**:

`str`: phase name

<a id="sunweg.device.Phase.voltage"></a>

#### voltage

```python
@property
def voltage() -> float
```

Get phase AC voltage in V.

**Returns**:

`float`: phase AC voltage in V

<a id="sunweg.device.Phase.amperage"></a>

#### amperage

```python
@property
def amperage() -> float
```

Get phase AC amperage in A.

**Returns**:

`float`: phase AC amperage in A

<a id="sunweg.device.Phase.status_voltage"></a>

#### status\_voltage

```python
@property
def status_voltage() -> Status
```

Get phase AC voltage status.

**Returns**:

`Status`: phase AC voltage status

<a id="sunweg.device.Phase.status_amperage"></a>

#### status\_amperage

```python
@property
def status_amperage() -> Status
```

Get phase AC amperage status.

**Returns**:

`Status`: phase AC amperage status

<a id="sunweg.device.Phase.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Cast Phase to str.

<a id="sunweg.device.String"></a>

## String Objects

```python
class String()
```

String details.

<a id="sunweg.device.String.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, voltage: float, amperage: float,
             status: Status) -> None
```

Initialize String.

**Arguments**:

- `name` (`str`): string name
- `voltage` (`float`): string DC voltage in V
- `amperage` (`float`): string DC amperage in A
- `status` (`Status`): string status

<a id="sunweg.device.String.name"></a>

#### name

```python
@property
def name() -> str
```

Get string name.

**Returns**:

`str`: string name

<a id="sunweg.device.String.voltage"></a>

#### voltage

```python
@property
def voltage() -> float
```

Get string DC voltage in V.

**Returns**:

`float`: string DC voltage in V

<a id="sunweg.device.String.amperage"></a>

#### amperage

```python
@property
def amperage() -> float
```

Get string DC amperage in A.

**Returns**:

`float`: string DC amperage in A

<a id="sunweg.device.String.status"></a>

#### status

```python
@property
def status() -> Status
```

Get string status.

**Returns**:

`Status`: string status

<a id="sunweg.device.String.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Cast String to str.

<a id="sunweg.device.MPPT"></a>

## MPPT Objects

```python
class MPPT()
```

MPPT details.

<a id="sunweg.device.MPPT.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str) -> None
```

Initialize MPPT.

**Arguments**:

- `name` (`srt`): MPPT name

<a id="sunweg.device.MPPT.name"></a>

#### name

```python
@property
def name() -> str
```

Get MPPT name.

**Returns**:

`str`: MPPT name

<a id="sunweg.device.MPPT.strings"></a>

#### strings

```python
@property
def strings() -> list[String]
```

Get list of MPPT's String.

**Returns**:

`list[String]`: list of Strings

<a id="sunweg.device.MPPT.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Cast MPPT to str.

<a id="sunweg.device.Inverter"></a>

## Inverter Objects

```python
class Inverter()
```

Inverter device.

<a id="sunweg.device.Inverter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(id: int,
             name: str,
             sn: str,
             status: Status,
             temperature: int,
             total_energy: float = 0,
             total_energy_metric: str = "",
             today_energy: float = 0,
             today_energy_metric: str = "",
             power_factor: float = 0,
             frequency: float = 0,
             power: float = 0,
             power_metric: str = "") -> None
```

Initialize Inverter.

**Arguments**:

- `id` (`int`): inverter id
- `name` (`str`): inverter name
- `sn` (`str`): inverter serial number
- `status` (`Status`): inverter status
- `temperature` (`int`): inverter temperature
- `total_energy` (`float`): total generated energy
- `total_energy_metric` (`str`): total generated energy metric
- `today_energy` (`float`): total generated energy today
- `today_energy_metric` (`str`): total generated energy today metric
- `power_factor` (`float`): inverter power factor
- `frequency` (`float`): inverter output frequency in Hz
- `power` (`str`): inverter output power
- `power` (`str`): inverter output power metric

<a id="sunweg.device.Inverter.id"></a>

#### id

```python
@property
def id() -> int
```

Get inverter id.

**Returns**:

`int`: inverter id

<a id="sunweg.device.Inverter.name"></a>

#### name

```python
@property
def name() -> str
```

Get inverter name.

**Returns**:

`str`: inverter name

<a id="sunweg.device.Inverter.sn"></a>

#### sn

```python
@property
def sn() -> str
```

Get inverter serial number.

**Returns**:

`str`: inverter serial number

<a id="sunweg.device.Inverter.status"></a>

#### status

```python
@property
def status() -> Status
```

Get inverter status.

**Returns**:

`Status`: inverter status

<a id="sunweg.device.Inverter.temperature"></a>

#### temperature

```python
@property
def temperature() -> int
```

Get inverter temperature.

**Returns**:

`int`: inverter temperature

<a id="sunweg.device.Inverter.today_energy"></a>

#### today\_energy

```python
@property
def today_energy() -> float
```

Get inverter today generated energy.

**Returns**:

`float`: inverter today generated energy

<a id="sunweg.device.Inverter.today_energy"></a>

#### today\_energy

```python
@today_energy.setter
def today_energy(value: float) -> None
```

Set inverter today generated energy.

**Arguments**:

- `value` (`float`): inverter today generated energy

<a id="sunweg.device.Inverter.today_energy_metric"></a>

#### today\_energy\_metric

```python
@property
def today_energy_metric() -> str
```

Get inverter today generated energy metric.

**Returns**:

`str`: inverter today generated energy metric

<a id="sunweg.device.Inverter.today_energy_metric"></a>

#### today\_energy\_metric

```python
@today_energy_metric.setter
def today_energy_metric(value: str) -> None
```

Set inverter today generated energy metric.

**Arguments**:

- `value` (`str`): inverter today generated energy metric

<a id="sunweg.device.Inverter.total_energy"></a>

#### total\_energy

```python
@property
def total_energy() -> float
```

Get inverter total generated energy.

**Returns**:

`float`: inverter total generated energy

<a id="sunweg.device.Inverter.total_energy"></a>

#### total\_energy

```python
@total_energy.setter
def total_energy(value: float) -> None
```

Set inverter total generated energy.

**Arguments**:

- `value` (`float`): inverter total generated energy

<a id="sunweg.device.Inverter.total_energy_metric"></a>

#### total\_energy\_metric

```python
@property
def total_energy_metric() -> str
```

Get inverter total generated energy metric.

**Returns**:

`str`: inverter total generated energy metric

<a id="sunweg.device.Inverter.total_energy_metric"></a>

#### total\_energy\_metric

```python
@total_energy_metric.setter
def total_energy_metric(value: str) -> None
```

Set inverter total generated energy metric.

**Arguments**:

- `value` (`str`): inverter total generated energy metric

<a id="sunweg.device.Inverter.power_factor"></a>

#### power\_factor

```python
@property
def power_factor() -> float
```

Get inverter power factor.

**Returns**:

`float`: inverter power factor

<a id="sunweg.device.Inverter.power_factor"></a>

#### power\_factor

```python
@power_factor.setter
def power_factor(value: float) -> None
```

Set inverter power factor.

**Arguments**:

- `value` (`float`): inverter power factor

<a id="sunweg.device.Inverter.frequency"></a>

#### frequency

```python
@property
def frequency() -> float
```

Get inverter frequency in Hz.

**Returns**:

`float`: inverter frequency in HZ

<a id="sunweg.device.Inverter.frequency"></a>

#### frequency

```python
@frequency.setter
def frequency(value: float) -> None
```

Set inverter frequency in Hz.

**Arguments**:

- `value` (`float`): inverter frequency in Hz

<a id="sunweg.device.Inverter.power"></a>

#### power

```python
@property
def power() -> float
```

Get inverter output power.

**Returns**:

`float`: inverter output power

<a id="sunweg.device.Inverter.power"></a>

#### power

```python
@power.setter
def power(value: float) -> None
```

Set inverter output power.

**Arguments**:

- `value` (`float`): inverter output power

<a id="sunweg.device.Inverter.power_metric"></a>

#### power\_metric

```python
@property
def power_metric() -> str
```

Get inverter output power metric.

**Returns**:

`str`: inverter output power metric

<a id="sunweg.device.Inverter.power_metric"></a>

#### power\_metric

```python
@power_metric.setter
def power_metric(value: str) -> None
```

Set inverter output power metric.

**Arguments**:

- `value` (`float`): inverter output power metric

<a id="sunweg.device.Inverter.is_complete"></a>

#### is\_complete

```python
@property
def is_complete() -> bool
```

Is inverter data complete.

**Returns**:

`bool`: True when inverter data is complete

<a id="sunweg.device.Inverter.phases"></a>

#### phases

```python
@property
def phases() -> list[Phase]
```

Get list of inverter's phases.

**Returns**:

`list[Phase]`: list of phases

<a id="sunweg.device.Inverter.mppts"></a>

#### mppts

```python
@property
def mppts() -> list[MPPT]
```

Get list of inverter's MPPTs.

**Returns**:

`list[MPPT]`: list of MPPTs

<a id="sunweg.device.Inverter.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Cast Inverter to str.

<a id="sunweg.plant"></a>

# sunweg.plant

Sunweg API plant.

<a id="sunweg.plant.Plant"></a>

## Plant Objects

```python
class Plant()
```

Plant details.

<a id="sunweg.plant.Plant.__init__"></a>

#### \_\_init\_\_

```python
def __init__(id: int, name: str, total_power: float, kwh_per_kwp: float,
             performance_rate: float, saving: float, today_energy: float,
             today_energy_metric: str, total_energy: float,
             total_carbon_saving: float, last_update: datetime) -> None
```

Initialize Plant.

**Arguments**:

- `id` (`int`): plant id
- `name` (`str`): plant name
- `total_power` (`float`): plant total power
- `kwh_per_kwp` (`float`): plant kWh/kWp
- `performance_rate` (`float`): plant performance rate
- `saving` (`float`): total saving in R$
- `today_energy` (`float`): today generated energy
- `today_energy_metric` (`str`): today generated energy metric
- `total_energy` (`float`): total generated energy in kWh
- `total_carbon_saving` (`float`): total of CO2 saved
- `last_update` (`datetime`): when the data was updated

<a id="sunweg.plant.Plant.id"></a>

#### id

```python
@property
def id() -> int
```

Get plant id.

**Returns**:

`int`: plant id

<a id="sunweg.plant.Plant.name"></a>

#### name

```python
@property
def name() -> str
```

Get plant name.

**Returns**:

`str`: plant name

<a id="sunweg.plant.Plant.total_power"></a>

#### total\_power

```python
@property
def total_power() -> float
```

Get plant total power.

**Returns**:

`float`: plant total power

<a id="sunweg.plant.Plant.kwh_per_kwp"></a>

#### kwh\_per\_kwp

```python
@property
def kwh_per_kwp() -> float
```

Get plant kWh/kWp.

**Returns**:

`float`: plant kWh/kWp

<a id="sunweg.plant.Plant.performance_rate"></a>

#### performance\_rate

```python
@property
def performance_rate() -> float
```

Get plant performance rate.

**Returns**:

`float`: plant performance rate

<a id="sunweg.plant.Plant.saving"></a>

#### saving

```python
@property
def saving() -> float
```

Get plant saving in R$.

**Returns**:

`float`: plant saving in R$

<a id="sunweg.plant.Plant.today_energy"></a>

#### today\_energy

```python
@property
def today_energy() -> float
```

Get plant today generated energy.

**Returns**:

`float`: plant today generated energy

<a id="sunweg.plant.Plant.today_energy_metric"></a>

#### today\_energy\_metric

```python
@property
def today_energy_metric() -> str
```

Get plant today generated energy metric.

**Returns**:

`str`: plant today generated energy metric

<a id="sunweg.plant.Plant.total_energy"></a>

#### total\_energy

```python
@property
def total_energy() -> float
```

Get plant total generated energy in kWh.

**Returns**:

`float`: plant total generated energy in kWh

<a id="sunweg.plant.Plant.total_carbon_saving"></a>

#### total\_carbon\_saving

```python
@property
def total_carbon_saving() -> float
```

Get plant total of CO2 saved.

**Returns**:

`float`: plant total of CO2 saved

<a id="sunweg.plant.Plant.last_update"></a>

#### last\_update

```python
@property
def last_update() -> datetime
```

Get when the plant data was updated.

**Returns**:

`datetime`: when the plant data was updated

<a id="sunweg.plant.Plant.inverters"></a>

#### inverters

```python
@property
def inverters() -> list[Inverter]
```

Get list of plant's inverters.

**Returns**:

`list[Inverter]`: list of inverters

<a id="sunweg.plant.Plant.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Cast Plant to str.

<a id="sunweg.api"></a>

# sunweg.api

API Helper.

<a id="sunweg.api.SunWegApiError"></a>

## SunWegApiError Objects

```python
class SunWegApiError(RuntimeError)
```

API Error.

<a id="sunweg.api.LoginError"></a>

## LoginError Objects

```python
class LoginError(SunWegApiError)
```

Login Error.

<a id="sunweg.api.APIHelper"></a>

## APIHelper Objects

```python
class APIHelper()
```

Class to call sunweg.net api.

<a id="sunweg.api.APIHelper.__init__"></a>

#### \_\_init\_\_

```python
def __init__(username: str, password: str) -> None
```

Initialize APIHelper for SunWEG platform.

**Arguments**:

- `username` (`str`): username for authentication
- `password` (`str`): password for authentication

<a id="sunweg.api.APIHelper.authenticate"></a>

#### authenticate

```python
def authenticate() -> bool
```

Authenticate with provided username and password.

**Returns**:

`bool`: True on authentication success

<a id="sunweg.api.APIHelper.listPlants"></a>

#### listPlants

```python
def listPlants(retry=True) -> list[Plant]
```

Retrieve the list of plants with incomplete inverter information.

You may want to call `complete_inverter()` to complete the Inverter information.

**Arguments**:

- `retry` (`bool`): reauthenticate if token expired and retry

**Returns**:

`list[Plant]`: list of Plant

<a id="sunweg.api.APIHelper.plant"></a>

#### plant

```python
def plant(id: int, retry=True) -> Plant | None
```

Retrieve plant detail by plant id.

**Arguments**:

- `id` (`int`): plant id
- `retry` (`bool`): reauthenticate if token expired and retry

**Returns**:

`Plant | None`: Plant or None if `id` not found.

<a id="sunweg.api.APIHelper.inverter"></a>

#### inverter

```python
def inverter(id: int, retry=True) -> Inverter | None
```

Retrieve inverter detail by inverter id.

**Arguments**:

- `id` (`int`): inverter id
- `retry` (`bool`): reauthenticate if token expired and retry

**Returns**:

`Inverter | None`: Inverter or None if `id` not found.

<a id="sunweg.api.APIHelper.complete_inverter"></a>

#### complete\_inverter

```python
def complete_inverter(inverter: Inverter, retry=True) -> None
```

Complete inverter data.

**Arguments**:

- `inverter` (`Inverter`): inverter object to be completed with information
- `retry` (`bool`): reauthenticate if token expired and retry

<a id="sunweg.util"></a>

# sunweg.util

Sunweg API util.

<a id="sunweg.util.Status"></a>

## Status Objects

```python
class Status(Enum)
```

Status enum.

