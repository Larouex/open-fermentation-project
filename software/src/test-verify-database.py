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

    # Initialization
    _verbose = False
    _module = "test-verify-database"
    _method = "main()"

    # execution state from args
    _parser = argparse.ArgumentParser()
    _parser.add_argument("-v", "--verbose", dest='verbose', action="store_true", help="Output Important information when executing.")
    _parser.add_argument("-d", "--debug", dest='debug', action="store_true", help="Output Debug information when executing.")
    args = _parser.parse_args()

    # gather parameters
    _verbose = args.verbose
    _debug = args.debug

    if _verbose:
        Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.INFO)
        Log.info("Verbose Logging Mode...")
    else:
        Log.basicConfig(format="%(levelname)s: %(message)s")

    if _debug:
        Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
        Log.info("Debug Logging Mode...")
    else:
        Log.basicConfig(format="%(levelname)s: %(message)s")

    # Load the configuration file
    _config = Config(Log)

    # Tracing and Errors
    _print_header = PrintHeader(Log, _verbose, _config)
    _print_error = PrintError(Log, _verbose, _config)

    # Load the recipes file
    _recipes = Recipes(Log)

    # Load the currentrecipe file
    _current_recipe = CurrentRecipe(Log)

    # verify locations
    _root_directory = os.path.dirname(os.path.abspath(__file__))
    _database_location = _root_directory + "\\" + _current_recipe.data["Database"]

    # test phases
    _recipephase = RecipePhase(Log, _verbose, _database_location, _current_recipe.data["Started"])
    _current_checkpoint = _current_recipe.data["Current Checkpoint"]

    # __Verbose__
    if (_verbose):
        _message = "Location: {location}".format(location = _database_location)
        _print_header.print(_module, _method, _message, False)
        _message = "Current Checkpoint: {checkpoint}".format(checkpoint = _current_checkpoint)
        _print_header.print(_module, _method, _message, True)

    # Show All Record from DB
    json_result = _recipephase.view_tracking_start_end()
    if json_result == None:
        print("---------------------------------------------------------------------")
        print("  SHOW ALL TRACKING RECORDS ERROR!!!")
        print("---------------------------------------------------------------------")
    else:
        _message = "(Tracking) From the Tracking table, the first row and last row..."
        _print_header.print(_module, _method, _message, True)
        _print_header.print(_module, _method, json_result, True)

    # Show Current Checkpoint Record from DB
    json_result = await _recipephase.select_tracking_by_checkpoint(_current_checkpoint)
    if json_result == None:
        print("---------------------------------------------------------------------")
        print("  SHOW CURRENT CHECKPOINT TRACKING RECORD IN FORMATTED JSON")
        print("  Checkpoint was not Found in tracking table")
        print("---------------------------------------------------------------------")
    else:
        _message = "(Tracking) Current Checkpoint from the Tracking table..."
        _print_header.print(_module, _method, _message, True)
        _print_header.print(_module, _method, json_result, True)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
