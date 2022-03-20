# ==================================================================================
#   File:   test-verify-relays.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Verify that the Relays are properly wired to the GPIO and cycling
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Software Design LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os, datetime
from distutils.command.config import config
from decimal import *
from gettext import NullTranslations
import logging as Log
import sqlite3
from sqlite3 import Error

# Our classes
from classes.config import Config
from classes.recipes import Recipes
from classes.currentrecipe import CurrentRecipe
from classes.recipephase import RecipePhase


# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

  # execution state from args
  verbose = False
  short_options = "hvd"
  long_options = ["help", "verbose", "debug"]
  full_cmd_arguments = sys.argv
  argument_list = full_cmd_arguments[1:]
  try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
  except getopt.error as err:
    print (str(err))

  for current_argument, current_value in arguments:

    if current_argument in ("-h", "--help"):
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("HELP for test-verify-database.py")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("")
      print("  BASIC PARAMETERS...")
      print("")
      print("  -h or --help - Print out this Help Information")
      print("  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging")
      print("  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      return

    if current_argument in ("-v", "--verbose"):
      verbose = True
      Log.basicConfig(format="%(levelname)s: %(message)s", level = Log.INFO)
      Log.info("Verbose Logging Mode...")
    else:
      Log.basicConfig(format="%(levelname)s: %(message)s")

    if current_argument in ("-d", "--debug"):
      Log.basicConfig(format="%(levelname)s: %(message)s", level = Log.DEBUG)
      Log.info("Debug Logging Mode...")
    else:
      Log.basicConfig(format="%(levelname)s: %(message)s")

  # Load the configuration file
  logger = Log
  config = Config(logger)
  config = config.data

  # Load the currentrecipe file
  current_recipe = CurrentRecipe(logger)
  current_recipe = current_recipe.data

  # verify locations
  root_directory = os.path.dirname(os.path.abspath(__file__))
  print("Root Directory:", root_directory)
  database_location = root_directory + "\\" + current_recipe["Database"]
  print("Database Location:", database_location)

  # test phases
  recipephase = RecipePhase(logger, database_location)
  current_checkpoint = current_recipe["Current Checkpoint"]
  print("Current Checkpoint:", current_checkpoint)

  # Show All Record from DB
  json_result = recipephase.view_tracking()
  if (json_result == None):
    print("---------------------------------------------------------------------")
    print("  SHOW ALL TRACKING RECORDS ERROR!!!")
    print("---------------------------------------------------------------------")
  else:
    print("---------------------------------------------------------------------")
    print("  SHOW ALL TRACKING RECORDS")
    print("---------------------------------------------------------------------")
    print(json_result)


  # Show Current Checkpoint Record from DB
  json_result = recipephase.select_tracking_by_checkpoint(current_checkpoint)
  if (json_result == None):
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
