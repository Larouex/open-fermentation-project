# ==================================================================================
#   File:   recipe.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Loads active recipe and provides lifecycle management
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, logging
import classes.constants as CONSTANT
import sqlite3


class Recipes:
    def __init__(self, logger):
        self.logger = logger
        self.load_file()

    def __init__(self, logger):
        self.logger = logger
        self.load_file()

    def load_file(self):
        with open("recipes.json", "r") as config_file:
            self.data = json.load(config_file)
            alerts = self.load_alerts()

            # self.logger.debug(alerts["Alerts"]["Recipes"]["Loaded"].format(self.data))

    def update_file(self, data):
        with open("recipes.json", "w") as configs_file:
            alerts = self.load_alerts()
            self.logger.debug(alerts["Alerts"]["Recipes"]["Updated"].format(self.data))
            configs_file.write(json.dumps(data, indent=2))

    def load_alerts(self):
        with open("recipes.json", "r") as alerts_file:
            return json.load(alerts_file)
