# ==================================================================================
#   File:   test-verify-database.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Verify that the Database is Correct and Working...
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import argparse, getopt, sys, time, string, threading, asyncio, os, datetime

#from distutils.command.config import config
from decimal import *
from gettext import NullTranslations
import logging as Log
import sqlite3
from sqlite3 import Error

# Our classes
from classes.config import Config
from classes.recipes import Recipes
from classes.recipes import Recipes
from classes.currentrecipe import CurrentRecipe
from classes.recipephase import RecipePhase
import classes.constants as CONSTANTS
from classes.printheader import PrintHeader
from classes.printerror import PrintError


# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

    # init
    _module = "test-verify-database"
    _method = "main()"

    # execution state from args
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Output important information when executing.")
    #parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    _verbose = args.verbose

    # Load the configuration file
    config = Config(Log)
    config_cache_data = config.data

    # Tracing and Errors
    _print_header = PrintHeader(Log, _verbose, config)
    _print_error = PrintError(Log, _verbose, config)

    # Load the currentrecipe file
    recipes = Recipes(Log)
    recipes_cache_data = recipes.data

    # Load the currentrecipe file
    current_recipe = CurrentRecipe(Log)
    current_recipe_cache_data = current_recipe.data

    # verify locations
    root_directory = os.path.dirname(os.path.abspath(__file__))
    database_location = root_directory + "\\" + current_recipe_cache_data["Database"]

    # __Verbose__
    if (_verbose):
        _message = "Root: {directory}".format(directory = root_directory)
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, False)
        _message = "Location: {location}".format(location = database_location)
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)

    # test phases
    recipephase = RecipePhase(Log, _verbose, database_location, current_recipe_cache_data["Started"])
    current_checkpoint = current_recipe_cache_data["Current Checkpoint"]

    # __Verbose__
    if (_verbose):
        _message = "Current Checkpoint: {checkpoint}".format(checkpoint = current_checkpoint)
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, False)

    # Show All Record from DB
    json_result = recipephase.view_tracking()
    if json_result == None:
        print("---------------------------------------------------------------------")
        print("  SHOW ALL TRACKING RECORDS ERROR!!!")
        print("---------------------------------------------------------------------")
    else:
        print("---------------------------------------------------------------------")
        print("  SHOW ALL TRACKING RECORDS")
        print("---------------------------------------------------------------------")
        print(json_result)

    # Show Current Checkpoint Record from DB
    json_result = await recipephase.select_tracking_by_checkpoint(current_checkpoint)
    if json_result == None:
        print("---------------------------------------------------------------------")
        print("  SHOW CURRENT CHECKPOINT TRACKING RECORD IN FORMATTED JSON")
        print("  Checkpoint was not Found in tracking table")
        print("---------------------------------------------------------------------")
    else:
        print("---------------------------------------------------------------------")
        print("  SHOW CURRENT CHECKPOINT TRACKING RECORD IN FORMATTED JSON")
        print("---------------------------------------------------------------------")
        print(json_result)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
