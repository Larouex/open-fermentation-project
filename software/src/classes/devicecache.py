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

class DeviceCache:

    def __init__(self, Log):
        
        # init
        self._filename = "devicecache.json"
        self._data = self.load_file()

    @property
    def data(self):
        return self._data

    def load_file(self):
        
        try:
            with open(self._filename, "r") as config_file:
                return json.load(config_file)
        
        except Exception as ex:
            print("DEVICECACHE ERROR: {}", ex)
        
        return 


    def update_file(self, data):

        try:
            with open(self._filename, "w") as configs_file:
                configs_file.write(json.dumps(data, indent=2))
        
        except Exception as ex:
            print("DEVICECACHE ERROR: {}", ex)
        
        return 
