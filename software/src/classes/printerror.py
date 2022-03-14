# ==================================================================================
#   File:   printerror.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Prints a error in all cases to the console for verbose debugging
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Software Design LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json
import logging

class PrintError:
    def __init__(self, Logger, Verbose):
        self._logger = Logger
        self._verbose = Verbose

    def print(self, module_name, method_name, message):

        if (self._verbose == true):
            print_message = " !!! ERROR MESSAGE !!!"
            print_message = " SCRIPT: {module_name}".format(module_name = module_name)
            print_message = " METHOD: {method_name}".format(method_name = method_name)
            print_message = " MESSAGE: {message}".format(message = message)
            print("")
            print("-------------------------------------------------")
            print(print_message)
            print("-------------------------------------------------")

        return 
