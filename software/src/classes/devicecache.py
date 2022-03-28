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
import json
import logging


class DeviceCache:
    def __init__(self, Log):
        self.logger = Log
        self.load_file()

    def load_file(self):
        with open("devicecache.json") as config_file:
            self.data = json.load(config_file)
            alerts = self.load_alerts()
            self.logger.debug(
                alerts["Alerts"]["DeviceCache"]["Loaded"].format(self.data)
            )

    def update_file(self, data):
        with open("devicecache.json", "w") as configs_file:
            alerts = self.load_alerts()
            self.logger.debug(
                alerts["Alerts"]["DeviceCache"]["Updated"].format(self.data)
            )
            configs_file.write(json.dumps(data, indent=2))

    def load_alerts(self):
        with open("alerts.json", "r") as alerts_file:
            return json.load(alerts_file)
