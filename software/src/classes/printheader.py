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

import classes.constants as CONSTANTS

class PrintHeader:
    def __init__(self, Logger, Verbose, Config):

        # init
        self._logger = Logger
        self._verbose = Verbose
        self._config_cache_data = Config.data

    def print(self, ModuleName, MethodName, Message, NoHeader):
        
        if self._verbose == True:
            print_message = "APP NAME: {app_name}\n".format(
                app_name = self._config_cache_data["AppName"]
            )
            print_message += "APP DESC: {app_desc}\n".format(
                app_desc = self._config_cache_data["Description"]
            )
            print_message += "SCRIPT: {module_name}\n".format(module_name = ModuleName)
            print_message += "METHOD: {method_name}".format(method_name = MethodName)
            
            # CONSTANTS.INFO
            if (NoHeader != True):
                print("")
                print("-------------------------------------------------------------")
                print(print_message)
                print("-------------------------------------------------------------")

            print_message = "{message}".format(message = Message)
            print(print_message)
            
        return

    def forceprint(self, Message):
        print_message = "{message}".format(message = Message)
        print(print_message)
        return

