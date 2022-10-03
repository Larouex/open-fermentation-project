# ==================================================================================
#   File:   dcmtemplate.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Handler for Config for the Gateway Device
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import json, logging
from pathlib import Path, PureWindowsPath

class DcmTemplate():
    
    def __init__(self, logger):
        self.logger = logger
        self.load_file()

    def load_file(self):
        with open('dcmtemplate.json', 'r') as config_file:
            self.data = json.load(config_file)
            alerts = self.load_alerts()
            self.logger.debug(alerts["Alerts"]["DcmTemplate"]["Loaded"].format(self.data))

    def update_file(self, fileName, data):
        path_to_file = Path(PureWindowsPath("DeviceTemplates\\{fileName}".format(fileName=fileName)))
        with open(path_to_file, 'w') as config_file:
            alerts = self.load_alerts() 
            config_file.write(json.dumps(data, indent=2))
            self.logger.debug(alerts["Alerts"]["DcmTemplate"]["Updated"].format(self.data))

    def load_alerts(self):
        with open('alerts.json', 'r') as alerts_file:
            return json.load(alerts_file)
