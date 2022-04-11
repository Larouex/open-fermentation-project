[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<a href="https://www.open-fermentation-project.org/"><img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen"></a>&nbsp;<a href="https://apps.azureiotcentral.com/">
<img src="https://img.shields.io/badge/Azure IoT Central-Open%20Fermentation%20Project%20v1-blue"></a>&nbsp;<a href="https://www.saluminator.com/">
<img src="https://img.shields.io/badge/IoT-Saluminator%20Appliance%20v4-purple"></a>

<img src="../assets/open-fermentation-project-logo-v2-750.png" width="250"/>

# Create Recipe Database

## Contents

- [Create Recipe Database](#create-recipe-database)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Script Parameters](#script-parameters)
  - [Details](#details)
  - [Database Details](#database-details)
    - [Details for the _tracking_ table](#details-for-the-tracking-table)
    - [Details for the _audit_ table](#details-for-the-audit-table)
    - [Details for the _relay_ table](#details-for-the-relay-table)
    - [Verify the Database](#verify-the-database)

## Overview

The Create Database script is the first script we run when we setup a new recipe for a fermentation cycle. The database technology we are using is based on SQLite and uses the Python sqllite package that is included in Python 3.x.

- **FILE**: <a href="./src/createdb.py">createdb.py</a>
- **LOCATION**: ./software/src/createdb.py
- **DEPENDANCIES**:
  - <a href="./src/recipes.json">recipes.json</a>
  - <a href="./src/currentrecipe.json">currentrecipe.json</a>
  - <a href="./src/config.json">config.json</a>
  - <a href="./src/alerts.json">alerts.json</a>

## Script Parameters

Let's look at all the options by running the script with --help option...

```bash
python ./createdb.py --help
```

<b>Output</b>

```bash
----------------------------------------------------------------------------------------------------------------
HELP for createdb.py
----------------------------------------------------------------------------------------------------------------

  BASIC PARAMETERS...

  -h or --help - Print out this Help Information
  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging
  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging

  REQUIRED PARAMETERS...

    -r or --recipename - The name provided must exist in the file named: recipes.json and is part of the
                          arrays of recipes that can be defined.
       USAGE: -r 'Salumi Toscano'
       USAGE: --recipename 'Salumi Toscano'
       DEFAULT: N/A, script will fail if not provided.

----------------------------------------------------------------------------------------------------------------
```

**Example**

```bash
python ./createdb.py --verbose --recipename 'Salumi Toscano'
```

## Details

The script executes the following actions...

- Loads the config.json file.
- Loads the recipes.json file.
- Creates the database file.
- Add the tables for the recipe life-cycle tracking, auditing, and the current status of the relays.
  - **Table names:** tracking, audit and relay
- Generate the fine grained “by hour” recipe entries into the recipe life-cycle tracking table.
- Add events for all database create activities to auditing table.

This fisrt parameter that gets filled in is the naming pattern for the database. This is verbose and it designed to make it easy to look at the file name and see the active recipe name. This items is located in the config.json file:

```json
"Database Naming Pattern": "active_recipe_{recipe_name}.db"
```

Based on the parameter passed into the script for --recipename, we first lookup that recipe and all of it's details from the recipes.json file. <a href="./createdb.py">Click here for</a>&nbsp;the details on the parameters in the recipes.json file and an detailed explanation of Recipe Management...

For example, we find **Salumi Toscano** in the recipe array...

```json
[
    {
      "Name": "Salumi Toscano",
      "Incubate": {
        "Cycle Time Toggle": 1,
        "Cycle Time": 12,
        "Temperature": {
          "Desired": 85,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        },
        "Humidity": {
          "Desired": 90,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        }
      },
      "Cure": {
        "Cycle Time Toggle": 24,
        "Cycle Time": 25,
        "Temperature": {
          "Desired": 60,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        },
        "Humidity": {
          "Desired": 75,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        }
      },
      "Finish": {
        "Cycle Time Toggle": 24,
        "Cycle Time": 10,
        "Temperature": {
          "Desired": 58,
          "Variance": 2,
          "Run Time": 3,
          "Idle Time": 5
        },
        "Humidity": {
          "Desired": 60,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        }
      }
    },
    {
        "Name": "Saucisson Sec", ...
    }
  ]
```

## Database Details

Once we create the database and the tables, the next step inserts not the database all of the individual, by hour "steps" that the lifecycle of the recipe will keep track of over time. We refer to these individual steps as **CHECKPOINTS** and the software keeps track of the place (the row in the database) that the recipe is at based on elapsed time since the recipe was started.

There is a json configuration file named **currentrecipe.json** located at the root folder. This file's purpose is to indicate the name of the active database, the date and time that the recipe was started and the current checkpoint of the recipe. The checkpoint is correlated to the number of elapased hour between the current date and time and the **Started** date and time.

**For example...**

```json
{
  "Database": "active_recipe.db",
  "Started": "2022-03-01 09:28:24.387745",
  "Current Checkpoint": 144
}
```

### Details for the _tracking_ table

The _tracking_ table represents the lifecycle of the recipe. When the database is created, the tracking table is populated with rows that represents data for every hour of the recipe.

[Click here for Recipe Managment Details](../RECIPES.MD)

Let's break down the content in the rows that get added. Examiing the **Incubation** entry for the **Salumi Toscano**, the following will be added...

- **Cycle Time Toggle** - The 1 represents measurement in _Hours_ (if the value is 24, that represents a _DAY_)
- **Cycle Time** - Length of time is _12 hours_
- **Temperature** - Desired chamber temperature is _85 degrees Fahrenheit_
- **Temperature Variance** - We can tolerate a _3 degrees above or below_ the desired _85 degrees Fahrenheit_
- **Temperature Run Time** - If the chamber temperature is _at or above 88 degrees or at or below 82 degress Fahrenheit_, then turn on the **Chiller Relay** to lower the temperature or turn on the **Heater Relay** to increase the temperature.
- **Humidity** - Desired chamber Humidity is _90 percent relative humidity_
- **Humidity Variance** - We can tolerate a _3 percent aboove of below of relative humidity_ to the desired _90 percent relative humidity_
- **Humidity Run Time** - If the chamber humidity is _at or above 93 percent relative humidity or at or below 88 percent relative humidity_, then turn on the **DeHumidifier Relay** to lower the humidity or turn on the **Humidifier Relay** to increase the humidity.
- **Humidity Idle Time** - If the time elapased since **DeHumidifier Relay** was turned on to lower the relative humidity or the **Humidifier Relay** was turned on to increase the relative humidity. The Idle time will pause for the indicated number of minutes before restting and engaging **humidity** control.

The json snippet below shows the actual configuration section in the **recipes.json** file that was explained in the above section.

```json
"Incubate": {
    "Cycle Time Toggle": 1,
    "Cycle Time": 12,
    "Temperature": {
        "Desired": 85,
        "Variance": 3,
        "Run Time": 3,
        "Idle Time": 5
    },
    "Humidity": {
        "Desired": 90,
        "Variance": 3,
        "Run Time": 3,
        "Idle Time": 5
}
```

This data is added to the database for the Incubation, Curing and Finishing section of the chosen recipe.

### Details for the _audit_ table

The _audit_ table captures the events that occur in the software. For example when the database is created, temperature changes that trigger a relay and so on. This table is used for auditing and troubleshooting issues that may arise. It is historical and sequential.

### Details for the _relay_ table

The _relay_ table is used to persist the state of a relay. For example, when the Temperature exceeds the desired + variance values, the relay for the Chiller will be engaged. The Relay table tracks starting time of the relay, measures the run time and idle time values and turns off the relay and resets the values for the next time.

### Verify the Database
There is a script included in the repository that provides verification to the database and helps look into the database and it's contents. In the \src directory, run the script below...

```bash
python .\test-verify-database.py -v
```

You should see something similar to the following output...

```bash
INFO: Verbose Logging Mode...

-------------------------------------------------------------
APP NAME: SaluminatorV4
APP DESC: Monitoring of Saluminator Fermentation System
SCRIPT: RecipePhase
METHOD: __init__
-------------------------------------------------------------
Today: 2022-04-11 14:22:22.755159
Recipe Started: 2022-04-11 13:54:34.802266
Hours Elapsed Since Recipe Started: 0

-------------------------------------------------------------
APP NAME: SaluminatorV4
APP DESC: Monitoring of Saluminator Fermentation System
SCRIPT: test-verify-database
METHOD: main()
-------------------------------------------------------------
Location: C:\Projects\open-fermentation-project\software\src\active_recipe_salumi_toscano.db
Current Checkpoint: 1
(Tracking) From the Tracking table, the first row and last row...
[{
	'id': 1,
	'recipe_phase': 'Incubate',
	'recipe_hour': 1,
	'completeness': '0.117785630153121323449028068353072740137577056884765625',
	'started_datetime': None,
	'completed_datetime': None,
	'temperature_format': 'F',
	'temperature_desired': 85,
	'temperature_variance': 3,
	'temperature_run_time': 3,
	'temperature_idle_time': 5,
	'humidity_desired': 90,
	'humidity_variance': 3,
	'humidity_run_time': 3,
	'humidity_idle_time': 5
}, {
	'id': 849,
	'recipe_phase': 'Finish',
	'recipe_hour': 849,
	'completeness': '0.117785630153121323449028068353072740137577056884765625',
	'started_datetime': None,
	'completed_datetime': None,
	'temperature_format': 'F',
	'temperature_desired': 58,
	'temperature_variance': 2,
	'temperature_run_time': 3,
	'temperature_idle_time': 5,
	'humidity_desired': 60,
	'humidity_variance': 3,
	'humidity_run_time': 3,
	'humidity_idle_time': 5
}]
(Tracking) Current Checkpoint from the Tracking table...
{
	'id': 1,
	'recipe_phase': 'Incubate',
	'recipe_hour': 1,
	'completeness': '0.117785630153121323449028068353072740137577056884765625',
	'started_datetime': None,
	'completed_datetime': None,
	'temperature_format': 'F',
	'temperature_desired': 85,
	'temperature_variance': 3,
	'temperature_run_time': 3,
	'temperature_idle_time': 5,
	'humidity_desired': 90,
	'humidity_variance': 3,
	'humidity_run_time': 3,
	'humidity_idle_time': 5
}
```