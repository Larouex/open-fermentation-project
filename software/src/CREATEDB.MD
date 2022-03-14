[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<a href="https://www.open-fermentation-project.org/"><img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen"></a>&nbsp;<a href="https://apps.azureiotcentral.com/">
<img src="https://img.shields.io/badge/Azure IoT Central-Open%20Fermentation%20Project%20v1-blue"></a>&nbsp;<a href="https://www.saluminator.com/">
<img src="https://img.shields.io/badge/IoT-Saluminator%20Appliance%20v4-purple"></a>

<img src="../../assets/open-fermentation-project-logo-v2_500px.png" width="300"/>

# Create Recipe Database

## Contents
- [Create Recipe Database](#create-recipe-database)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Script Parameters](#script-parameters)
  - [Details](#details)

<img src="../../assets/python-icon.png" width="50" class="pull-left"/>

## Overview
The Create Database script is the first script we run when we setup a new recipe for a fermentation cycle.  The database technology we are using is based on SQLite and uses the Python sqllite package that is included in Python 3.x.

- **FILE**: <a href="./createdb.py">createdb.py</a>
- **DEPENDANCIES**: 
  - <a href="./recipes.json">recipes.json</a>
  - <a href="./currentrecipe.json">currentrecipe.json</a>
  - <a href="./config.json">config.json</a>

## Script Parameters

  **Basic**
  - -h or --help - Print out this Help Information
  - -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging
  - -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging

  **Required**
  - -r or --recipename - The name provided must exist in the file named 'recipes.json' and is part of the arrays of recipes that can be defined.
  **USAGE:** -r 'Salumi Toscano' OR --recipename 'Salumi Toscano'
  **DEFAULT:** N/A, script will fail if not provided.
  
  **Example**
  ````bash
  (src)$ python createdb.py --verbose --recipename 'Salumi Toscano'
  ````

## Details
The script executes the following actions when ran...

- Create the Database
- Add the tables for the recipe life-cycle tracking, auditing, and the current relay status.
- Generate the fine grained “by hour” recipe entries into the recipe life-cycle tracking table.
- Add events for all database create activities to Audit table.

This fisrt parameter that gets filled in is the naming pattern for the database. This is verbose and it designed to make it easy to look at the file name and see the active recipe name. This items is located in the config.json file:

````json
"DatabaseNamingPattern": "active_recipe_{recipe_name}.db"
````
Based on the parameter passed into the script for --recipename, we first lookup that recipe and all of it's details from the recipes.json file. <a href="./createdb.py">CLick here for</a>&nbsp;the details on the parameters in the recipes.json file and an detailed explanation of Recipe Management...

For example, we find [Salumi Toscano] in the recipe array...

````json
[
    {
      "Name": "Salumi Toscano",
      "Incubate": {
        "Cycle Time Toggle": 1,
        "Cycle Time": 18,
        "Temperature": {
          "Desired": 77,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        },
        "Humidity": {
          "Desired": 80,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        }
      },
      "Cure": {
        "Cycle Time Toggle": 24,
        "Cycle Time": 25,
        "Temperature": {
          "Desired": 62,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        },
        "Humidity": {
          "Desired": 65,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        }
      },
      "Finish": {
        "Cycle Time Toggle": 24,
        "Cycle Time": 10,
        "Temperature": {
          "Desired": 60,
          "Variance": 2,
          "Run Time": 3,
          "Idle Time": 5
        },
        "Humidity": {
          "Desired": 75,
          "Variance": 3,
          "Run Time": 3,
          "Idle Time": 5
        }
      }
    }
  ]
  ````
