# ==================================================================================
#   File:   printheader.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Prints a header to the console for verbose debugging
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, logging, pprint

from classes.config import Config
import classes.constants as CONSTANTS

class PrintHeader:
    def __init__(self, Logger, Verbose):

        # init
        self._logger = Logger
        self._verbose = Verbose

        # Load the configuration file
        self._config = Config(self._logger, self._verbose)
        self._config = self._config.data

    def print(self, ModuleName, MethodName, Message, MessageType, NoHeader):
        
        if self._verbose == True:
            print_message = "VERBOSE MESSAGE\n"
            print_message += "APP NAME: {app_name}\n".format(
                app_name = self._config["AppName"]
            )
            print_message += "APP DESC: {app_desc}\n".format(
                app_desc = self._config["Description"]
            )
            print_message += "SCRIPT: {module_name}\n".format(module_name = ModuleName)
            print_message += "METHOD: {method_name}".format(method_name = MethodName)
            
            # CONSTANTS.INFO
            if (NoHeader != True):
                print("")
                print("-------------------------------------------------")
                print(print_message)
                print("-------------------------------------------------")

            print_message = "{message}".format(message = Message)
            pp = pprint.PrettyPrinter(indent=2, width=80, compact=True)
            pp.pprint(print_message)
            
        return

