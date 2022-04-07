# ==================================================================================
#   File:   config.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Handler for Config
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, logging

class Config:

    def __init__(self, Logger, Verbose):

        # init
        self._logger = Logger
        self._verbose = Verbose

        # Load the configuration
        self.load_file()

    def load_file(self):
        with open("config.json", "r") as config_file:
            self.data = json.load(config_file)
            
            if (self._verbose == True):
                alerts = self.load_alerts()
                self._logger.debug(alerts["Alerts"]["Config"]["Loaded"].format(self.data))

            return

    def update_file(self, data):
        with open("config.json", "w") as configs_file:
               
            configs_file.write(json.dumps(data, indent=2))

            if (self._verbose == True):
                alerts = self.load_alerts()
                self.logger.debug(alerts["Alerts"]["Config"]["Updated"].format(self.data))

            return

    def load_alerts(self):
        with open("alerts.json", "r") as alerts_file:
            return json.load(alerts_file)

