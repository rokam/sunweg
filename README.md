# SunWeg
Python lib for WEG solar energy platform, https://sunweg.net/

# Usage

```
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

# Contribute
Feel free to send issues and pull requests.