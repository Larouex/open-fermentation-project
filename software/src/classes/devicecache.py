# ==================================================================================
#   File:   config.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    SaS key class for all operations on connections and generation of
#           keys used to connect via DPS and Azure IoT Central
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, logging
import classes.constants as CONSTANTS
from classes.printheader import PrintHeader
from classes.printerror import PrintError

class DeviceCache:
    def __init__(self, Log, Verbose):
        
        # init
        self._print_header = PrintHeader(Log, Verbose)
        self._print_error = PrintError(Log, Verbose)
        self._module = "DeviceCache"
        self._method = None

        self.logger = Log
        self.load_file()

    def load_file(self):
        self._method = "load_file"
        try:

            with open("devicecache.json") as config_file:
                self.data = json.load(config_file)
                alerts = self.load_alerts()
                self.logger.debug(
                    alerts["Alerts"]["DeviceCache"]["Loaded"].format(self.data)
                )
        
        except Exception as ex:
            self._print_error.print(self._module, self._method, ex)
        
        return 

    def update_file(self, data):
        self._method = "update_file"
        try:

            with open("devicecache.json", "w") as configs_file:
                alerts = self.load_alerts()
                self.logger.debug(
                    alerts["Alerts"]["DeviceCache"]["Updated"].format(self.data)
                )
                configs_file.write(json.dumps(data, indent=2))

        except Exception as ex:
            self._print_error.print(self._module, self._method, ex)
        
        return 

    def load_alerts(self):
        self._method = "load_alerts"
        try:
            with open("alerts.json", "r") as alerts_file:
                return json.load(alerts_file)
        
        except Exception as ex:
            self._print_error.print(self._module, self._method, ex)
        
        return 
