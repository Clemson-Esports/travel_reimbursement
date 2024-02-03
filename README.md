# travel_reimbursement
Script that creates a GUI to calculate reimbursable costs of a trip.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

This is the tool that Clemson Esports uses to calculate the reimbursable cost of a trip.

To encourage carpooling and driving efficient cars, we apply a multiplier to the expected cost of your trip.

For example, if you drive a sedan, we expect you to drive at least one another person, as well as have a gas mileage of 35 mpg. If you have less gas mileage, you will only be reimbursed a proportional percentage of your trip (relative to the expected gas mileage), and similarly for the number of occupants in the vehicle.

## Installing and using the executable

To recreate this executable, run (assuming you have Python on your machine):

```bash
pip install pyinstaller
pyinstaller --onefile reimburse.py
```

which will create an executable at [dist/reimburse.exe](https://github.com/Clemson-Esports/travel_reimbursement/blob/main/dist/reimburse.exe). Or, alternatively, click [here](https://github.com/Clemson-Esports/travel_reimbursement/archive/refs/heads/main.zip) to download the entire repository, and open the executable `travel_reimbursement-main/dist/reimburse.exe` if you trust it.

This will open an example window which you can use to see reimbursable amounts for a trip.

In the top left window, there will be a configuration text box that defines the settings of the calculation. The default settings are:

```json
{
    "total_miles": 300,
    "gas_per_gal": 2.75,
    "vehicle_classes": [
        "sedan",
        "suv"
    ],
    "expected_mpg": {
        "sedan": 35,
        "suv": 30
    },
    "max_occupants": {
        "sedan": 2,
        "suv": 3
    }
}
```

which says that the trip is 300 miles, the current price of gas is $2.75 per gallon, there are two vehicle types to account for (sedan and SUV), the expected gas mileages are 35 mpg for sedans and 30 mpg for SUVs, and that the expected/maximum number of occupants is 2 for sedans and 3 for SUVs. Press "Enter" on the Configuration button to enter settings.

**IMPORTANT**: These might not be the settings that current Officers are using, so be sure to ask.

In the top right window, there are trips to enter. This defaults to:

```
Sedan 2 30
SUV 3 25
```

which says that two trips happened: one in a Sedan with 2 people that costed $30, and one in an SUV with 3 people that costed $35. You can enter any number of trips here, and the vehicle type is not case-sensitive, it just must be defined in the settings. Press "Enter" on the Trips button to calculate the reimbursable costs, which will display in the bottom window.