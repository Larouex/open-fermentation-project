# ==================================================================================
#   File:   server.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    When the OpcServer starts, this file written out as a map to the
#           node ids to the telemetry so we pull them via Node Id's
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json
import logging


class MapTelemetry:
    def __init__(self, Log):
        self.logger = Log
        self.data = []

    def load_file(self):
        with open("maptelemetry.json", "r") as config_file:
            self.data = json.load(config_file)
            alerts = self.load_alerts()
            self.logger.info(
                alerts["Alerts"]["MapTelemetry"]["Loaded"].format(self.data)
            )

    def update_file(self, data):
        self.data = data
        with open("maptelemetry.json", "w") as config_file:
            alerts = self.load_alerts()
            config_file.write(json.dumps(data, indent=2))
            self.logger.debug(
                alerts["Alerts"]["MapTelemetry"]["Updated"].format(self.data)
            )

    def load_alerts(self):
        with open("alerts.json", "r") as alerts_file:
            return json.load(alerts_file)
