# ==================================================================================
#   File:   printerror.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Prints a error in all cases to the console for verbose debugging
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, logging

class PrintError:
    
    def __init__(self, Logger, Verbose, Config):

        # init
        self._logger = Logger
        self._verbose = Verbose

        # Load the configuration file
        self._config = Config
        self._config_cache_data = self._config.data

    def print(self, module_name, method_name, message):

        if self._verbose == True:
            print_message = "!!! ERROR MESSAGE !!!\n"
            print_message += "APP NAME: {app_name}\n".format(
                app_name=self._config_cache_data["AppName"]
            )
            print_message += "APP DESC: {app_desc}\n".format(
                app_desc=self._config_cache_data["Description"]
            )
            print_message += "SCRIPT: {module_name}\n".format(module_name=module_name)
            print_message += "METHOD: {method_name}".format(method_name=method_name)
            print("")
            print("-------------------------------------------------")
            print(print_message)
            print("-------------------------------------------------")
            print_message = "MESSAGE: {message}".format(message=message)
            print(print_message)
            print("")

        return
