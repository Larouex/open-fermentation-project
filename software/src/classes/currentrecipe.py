# ==================================================================================
#   File:   currentrecipe.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Handler for CurrentRecipe.json
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json
import logging


class CurrentRecipe:
    def __init__(self, Logger, Verbose):
        self._logger = Logger
        self._verbose = Verbose
        self.load_file()

    @property
    def data(self):
        return self._data

    def load_file(self):

        with open("currentrecipe.json", "r") as config_file:

            self._data = json.load(config_file)
            alerts = self.load_alerts()
            self._logger.debug(
                alerts["Alerts"]["CurrentRecipe"]["Loaded"].format(self.data)
            )

            if self._verbose == True:
                print("")
                print("-------------------------------------------------")
                print(" CurrentRecipe.py::load_file")
                print("-------------------------------------------------")
                print("Data->", self._data)

    def update_file(self, data):

        with open("currentrecipe.json", "w") as configs_file:

            alerts = self.load_alerts()
            self._logger.debug(
                alerts["Alerts"]["CurrentRecipe"]["Updated"].format(data)
            )

            if self._verbose == True:
                print("")
                print("-------------------------------------------------")
                print(" CurrentRecipe.py::update_file")
                print("-------------------------------------------------")
                print("Data->", data)

            configs_file.write(json.dumps(data, indent=2))

    def load_alerts(self):
        with open("alerts.json", "r") as alerts_file:
            return json.load(alerts_file)
