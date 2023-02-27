# SunWeg

[![Python build](https://github.com/rokam/sunweg/actions/workflows/python-build.yml/badge.svg)](https://github.com/rokam/sunweg/actions/workflows/python-build.yml)
![Python tests](https://raw.githubusercontent.com/rokam/sunweg/badges/tests.svg)
![Python coverage](https://raw.githubusercontent.com/rokam/sunweg/badges/coverage.svg)
![Python fake8](https://raw.githubusercontent.com/rokam/sunweg/badges/flake8.svg)

Python lib for WEG solar energy platform, https://sunweg.net/

## Usage

``` python
from sunweg.api import APIHelper

api = APIHelper('username','password')
plants = api.listPlants()
for plant in plants:
    print(plant)
    for inverter in plant.inverters:
        print(inverter)
        for phase in inverter.phases:
            print(phase)
        for mppt in inverter.mppts:
            print(mppt)
            for string in mppt.strings:
                print(string)
```

## Documentation

Check the [DOCs](https://github.com/rokam/sunweg/blob/main/docs/index.md) for API documentation.

## Contribute

Feel free to send issues and pull requests.
