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


class DcmTemplate:
    def __init__(self, Log):

        # init
        self._filename = "dcmtemplate.json"
        self._data = self.load_file()

    @property
    def data(self):
        return self._data

    def load_file(self):

        try:
            with open(self._filename, "r") as config_file:
                return json.load(config_file)

        except Exception as ex:
            print("DCMTEMPLATE ERROR: {}", ex)

        return

    def update_file(self, data):

        try:
            with open(self._filename, "w") as configs_file:
                configs_file.write(json.dumps(data, indent=2))

        except Exception as ex:
            print("DCMTEMPLATE ERROR: {}", ex)

        return
