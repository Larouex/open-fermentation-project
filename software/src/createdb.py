#!/usr/bin/env python
# # ==================================================================================
#   File:   createdb.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Creates a Recipe Database for a new Fermentation Recipe Lifecycle
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import argparse, getopt, sys, time, string, threading, asyncio, os
from datetime import datetime, date
#from distutils.command.config import config
from decimal import *
from gettext import NullTranslations
import logging as Log
import sqlite3
from sqlite3 import Error

# Our classes
from classes.config import Config
from classes.recipes import Recipes
from classes.currentrecipe import CurrentRecipe
from classes.printtracing import PrintTracing

# -------------------------------------------------------------------------------
#   Function:   create_connection
#   Usage:      Create connection helper
# -------------------------------------------------------------------------------
def create_connection(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print("Exception::createdb.py(create_connection)->", e)

    return conn


# -------------------------------------------------------------------------------
#   Function:   create_table
#   Usage:      Create table helper
# -------------------------------------------------------------------------------
def create_table(conn, create_table_sql):

    try:
        c = conn.cursor()
        c.execute(create_table_sql)

    except Error as e:
        print("Exception::createdb.py(create_table)->", e)

    return


# -------------------------------------------------------------------------------
#   Function:   create_tracking
#   Usage:      Inserts the recipe checkpoints into the database
# -------------------------------------------------------------------------------
def create_tracking(conn, task):

    try:

        sql = """ INSERT INTO tracking(
                    recipe_phase,
                    recipe_hour,
                    completeness,
                    started_datetime,
                    completed_datetime,
                    temperature_format,
                    temperature_desired,
                    temperature_variance,
                    temperature_run_time,
                    temperature_idle_time,
                    humidity_desired,
                    humidity_variance,
                    humidity_run_time,
                    humidity_idle_time)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
        # 1,2,3,4,5,6,7,8,9,0,1,2,3,4
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()

        return cur.lastrowid

    except Exception as e:
        print("Exception::createdb.py(create_tracking)->", e)
        return None


# -------------------------------------------------------------------------------
#   Function:   get_tracking_table_definition
#   Usage:      Tracking Table Definition
# -------------------------------------------------------------------------------
def get_tracking_table_definition():
    sql_table_description = """ CREATE TABLE IF NOT EXISTS tracking (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    recipe_phase TEXT NOT NULL,
                                    recipe_hour INTEGER NOT NULL,
                                    completeness TEXT NOT NULL,
                                    started_datetime TEXT NULL,
                                    completed_datetime TEXT NULL,
                                    temperature_format TEXT NULL,
                                    temperature_desired INTEGER NOT NULL,
                                    temperature_variance INTEGER NOT NULL,
                                    temperature_run_time INTEGER NOT NULL,
                                    temperature_idle_time INTEGER NOT NULL,
                                    humidity_desired INTEGER NOT NULL,
                                    humidity_variance INTEGER NOT NULL,
                                    humidity_run_time INTEGER NOT NULL,
                                    humidity_idle_time INTEGER NOT NULL
                                ); """
    return sql_table_description


# -------------------------------------------------------------------------------
#   Function:   get_audit_table_definition
#   Usage:      Audit Table Definition
# -------------------------------------------------------------------------------
def get_audit_table_definition():
    sql_table_description = """ CREATE TABLE IF NOT EXISTS audit (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    recipe_phase TEXT NOT NULL,
                                    recipe_hour INTEGER NOT NULL,
                                    event_datetime TEXT NOT NULL,
                                    event_type TEXT NOT NULL,
                                    event_description TEXT NOT NULL
                                ); """
    return sql_table_description


# -------------------------------------------------------------------------------
#   Function:   get_relay_table_definition
#   Usage:      Audit Table Definition
# -------------------------------------------------------------------------------
def get_relay_table_definition():
    sql_table_description = """ CREATE TABLE IF NOT EXISTS relay (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    recipe_phase TEXT NOT NULL,
                                    recipe_hour INTEGER NOT NULL,
                                    event_datetime TEXT NOT NULL,
                                    event_type TEXT NOT NULL,
                                    event_description TEXT NOT NULL
                                ); """
    return sql_table_description


# -------------------------------------------------------------------------------
#   Function:   audit_event
#   Usage:      Insert Audit event into the database
# -------------------------------------------------------------------------------
def audit_event(conn, task):

    try:

        sql = """ INSERT INTO audit(
                    recipe_phase,
                    recipe_hour,
                    event_datetime,
                    event_type,
                    event_description)
                VALUES(?,?,?,?,?) """

        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()

        return cur.lastrowid

    except Exception as e:
        print("Exception::createdb.py(audit_event)->", e)
        return None

# -------------------------------------------------------------------------------
#   Function:   create_current_recipe
#   Usage:      Returns a json Object to Update Current Recipe
# -------------------------------------------------------------------------------
def create_current_recipe(DBFileName, ActiveRecipeName, Started):
    newRecipe = {
        "Database": DBFileName,
        "Started": Started,
        "Recipe Name": ActiveRecipeName,
        "Current Checkpoint": 1
    }

    return newRecipe


# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

    # execution state from args
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", dest='verbose', action="store_true", help="Output important information when executing.")
    parser.add_argument("-r", "--recipename", dest='recipename', help="Indicate the Recipe Name that exists in the recipes.json File.")
    #parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    _verbose = args.verbose
    _recipe_name = args.recipename

    if _recipe_name != None:
        Log.info(
            "Recipe name is specified as: {recipename}".format(
                recipename = _recipe_name
            )
        )
    else:
        # Missing Recipe Name. It is required, so fail
        print(
            "[ERROR] -r --recipename must be specified and match a recipe name in recipes.json."
        )
        return

    # Load the configuration file
    _config = Config(Log)

    # Messaging
    _printtracing = PrintTracing(Log, _verbose, _config)

    # Get the recipes array from the recipes.json file
    _recipes = Recipes(Log)

    # validate names and file naming pattern
    _existing_recipe = [x for x in _recipes.data if x["Name"] == _recipe_name]
    if len(_existing_recipe) == 0:
        # Missing Recipe Name in recipes.json. It is required, so fail
        print("[ERROR] -r --recipename must match a recipe name in recipes.json.")
        return

    # create the file name
    _database_file_name = _config.data["Database Naming Pattern"].format(recipe_name = _recipe_name.replace(" ", "_").lower())

    # Database - Create file name
    _current_date_and_time = datetime.now()
    _current_date_and_time_string = str(_current_date_and_time)

    # Load the currentrecipe file
    _current_recipe = CurrentRecipe(Log)

    # create con object to connect
    _root_directory = os.path.dirname(os.path.abspath(__file__))
    _database_location = _root_directory + "//" + _database_file_name
    _conn = create_connection(_database_location)
    
    print("Root Directory:", _root_directory)
    print("Database Location:", _database_location)

    if _conn is not None:
        # create tracking table
        create_table(_conn, get_tracking_table_definition())

        # create audit table
        create_table(_conn, get_audit_table_definition())

    else:
        print("Error! cannot create the database connection.")

    # Register completion Audit Event
    _audit_event_1 = (
        "DATABASE",
        0,
        datetime.now(),
        "CREATED",
        "Completed Database Creation.",
    )
    audit_event(_conn, _audit_event_1)

    # init the values
    _completeness = 0
    _recipe_hour = 1

    # Lets Populate the Checkpoint Activities
    for _recipe in _recipes.data:
        
        if _recipe["Name"] == _recipe_name:

            print("-------------------------------------------------------")
            print("Found Recipe...")

            # Gather Times and Build Up Meta Data
            _incubate_toggle = _recipe["Incubate"]["Cycle Time Toggle"]
            _incubate_time = _recipe["Incubate"]["Cycle Time"]
            _cure_toggle = _recipe["Cure"]["Cycle Time Toggle"]
            _cure_time = _recipe["Cure"]["Cycle Time"]
            _finish_toggle = _recipe["Finish"]["Cycle Time Toggle"]
            _finish_time = _recipe["Finish"]["Cycle Time"]

            # create loop numbers
            _incubate_loop = (_incubate_toggle * _incubate_time) - 1
            _cure_loop = (_cure_toggle * _cure_time) - 1
            _finish_loop = (_finish_toggle * _finish_time) - 1

            # Completeness - Based on all hours, percent of 100
            _completeness_value = Decimal(
                100 / (_incubate_loop + _cure_loop + _finish_loop)
            )

            print(" Completeness=", _completeness_value)

            # Incubate
            print(" Creating Incubation Lifecycle...")
            for x in range(0, _incubate_loop):
                _tracking_incubation = (
                    "Incubate",
                    _recipe_hour,
                    str(_completeness_value),
                    None,
                    None,
                    "F",
                    _recipe["Incubate"]["Temperature"]["Desired"],
                    _recipe["Incubate"]["Temperature"]["Variance"],
                    _recipe["Incubate"]["Temperature"]["Run Time"],
                    _recipe["Incubate"]["Temperature"]["Idle Time"],
                    _recipe["Incubate"]["Humidity"]["Desired"],
                    _recipe["Incubate"]["Humidity"]["Variance"],
                    _recipe["Incubate"]["Humidity"]["Run Time"],
                    _recipe["Incubate"]["Humidity"]["Idle Time"],
                )
                create_tracking(_conn, _tracking_incubation)
                _recipe_hour = _recipe_hour + 1

            # Cure
            print(" Creating Cure Lifecycle...")
            for x in range(0, _cure_loop):
                _tracking_cure = (
                    "Cure",
                    _recipe_hour,
                    str(_completeness_value),
                    None,
                    None,
                    "F",
                    _recipe["Cure"]["Temperature"]["Desired"],
                    _recipe["Cure"]["Temperature"]["Variance"],
                    _recipe["Cure"]["Temperature"]["Run Time"],
                    _recipe["Cure"]["Temperature"]["Idle Time"],
                    _recipe["Cure"]["Humidity"]["Desired"],
                    _recipe["Cure"]["Humidity"]["Variance"],
                    _recipe["Cure"]["Humidity"]["Run Time"],
                    _recipe["Cure"]["Humidity"]["Idle Time"],
                )
                create_tracking(_conn, _tracking_cure)
                _recipe_hour = _recipe_hour + 1

            # Finish
            print(" Creating Finish Lifecycle...")
            for x in range(0, _finish_loop):
                _completeness = 1
                _tracking_finish = (
                    "Finish",
                    _recipe_hour,
                    str(_completeness_value),
                    None,
                    None,
                    "F",
                    _recipe["Finish"]["Temperature"]["Desired"],
                    _recipe["Finish"]["Temperature"]["Variance"],
                    _recipe["Finish"]["Temperature"]["Run Time"],
                    _recipe["Finish"]["Temperature"]["Idle Time"],
                    _recipe["Finish"]["Humidity"]["Desired"],
                    _recipe["Finish"]["Humidity"]["Variance"],
                    _recipe["Finish"]["Humidity"]["Run Time"],
                    _recipe["Finish"]["Humidity"]["Idle Time"],
                )
                create_tracking(_conn, _tracking_finish)
                _recipe_hour = _recipe_hour + 1

        # Register completion Audit Event
        _audit_event_2 = (
            "CREATE",
            0,
            datetime.now(),
            "TRACKING",
            "Completed Recipe Tracking Insertion of all Checklpoints into the Database.",
        )
        audit_event(_conn, _audit_event_2)

        print("Completed!")
        print("-------------------------------------------------------")

        # Update current recipe file
        _current_recipe.update_file(create_current_recipe(_database_file_name, _recipe_name, _current_date_and_time_string))

        break
    else:
        index = index + 1


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
