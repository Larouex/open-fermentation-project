# ==================================================================================
#   File:   simulate.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Encapsulates the simulation of the telemetry for Temp and Humidity
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, logging, random
import classes.constants as CONSTANT

class Simulate:
    def __init__(self, Log, Verbose, Config):
        self.logger = Log
        self._verbose = Verbose

        # Load the configuration file
        self._config = Config
        self._config_cache_data = self._config.data

        # Properties
        self._ambient_temperature = 0
        self._ambient_humdity = 0
        self._chamber_temperature = 0
        self._chamber_humdity = 0

        # State
        self._last_ambient_temperature = 0
        self._last_ambient_humdity = 0
        self._last_chamber_temperature = 0
        self._last_chamber_humdity = 0

    @property
    def ambient_temperature(self):
        return self._ambient_temperature

    @property
    def ambient_humdity(self):
        return self._ambient_humdity

    @property
    def chamber_temperature(self):
        return self._chamber_temperature

    @property
    def chamber_humdity(self):
        return self._chamber_humdity

    def RunSimulation(self):

        self._last_ambient_temperature = self._ambient_temperature
        self._last_ambient_humdity = self._ambient_humdity
        self._last_chamber_temperature = self._chamber_temperature
        self._last_chamber_humdity = self._chamber_humdity

        self._ambient_temperature = self.get_ambient_temperature()
        self._ambient_humdity = self.get_ambient_humdity()
        self._chamber_temperature = self.get_chamber_temperature()
        self._chamber_humdity = self.get_chamber_humdity()
        return

    def get_ambient_temperature(self):            
        _min = self._config_cache_data["Simulation"]["Ambient Temperature"]["Minimum"]
        _max = self._config_cache_data["Simulation"]["Ambient Temperature"]["Maximum"]
        _value = random.uniform(_min, _max)
        return _value

    def get_ambient_humdity(self):            
        _min = self._config_cache_data["Simulation"]["Ambient Humidity"]["Minimum"]
        _max = self._config_cache_data["Simulation"]["Ambient Humidity"]["Maximum"]
        _size = 1
        _value = [random.randint(_min, _max) for _ in range(_size)]
        return int(_value[0])

    def get_chamber_temperature(self):            
        _min = self._config_cache_data["Simulation"]["Chamber Temperature"]["Minimum"]
        _max = self._config_cache_data["Simulation"]["Chamber Temperature"]["Maximum"]
        _value = random.uniform(_min, _max)
        return _value

    def get_chamber_humdity(self):            
        _min = self._config_cache_data["Simulation"]["Chamber Humidity"]["Minimum"]
        _max = self._config_cache_data["Simulation"]["Chamber Humidity"]["Maximum"]
        _size = 1
        _value = [random.randint(_min, _max) for _ in range(_size)]
        return int(_value[0])
