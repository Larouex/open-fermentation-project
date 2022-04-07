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

    def __init__(self, Log):
        
        # init
        self._filename = "config.json"
        self._data = self.load_file()

    @property
    def data(self):
        return self._data

    def load_file(self):
        
        try:
            with open(self._filename, "r") as config_file:
                return json.load(config_file)
        
        except Exception as ex:
            print("CONFIG ERROR: {}", ex)
        
        return 


    def update_file(self, data):

        try:
            with open(self._filename, "w") as configs_file:
                configs_file.write(json.dumps(data, indent=2))
        
        except Exception as ex:
            print("CONFIG ERROR: {}", ex)
        
        return 
