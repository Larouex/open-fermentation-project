# ==================================================================================
#   File:   relay.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Base characteristics of the AC Relays used for controlling
#           Saluminator system like Hundifier, DeHumdifier, Heater, Chiller
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Software Design LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, logging
import classes.constants as CONSTANT
import RPi.GPIO as GPIO


class Relay:
    def __init__(self, Log, Verbose, IOPin, State):
        self.logger = Log

        self._verbose = Verbose
        self._ioPin = IOPin
        self._state = State

        # init pins
        GPIO.setup(self._ioPin, GPIO.OUT)
        self.setRelayState(self._state)

    @property
    def state(self):
        return self._state

    def setRelayState(self, State):

        self._state = State

        try:
            if self._state == CONSTANT.ON:
                GPIO.output(self._ioPin, GPIO.HIGH)

            elif self._state == CONSTANT.OFF:
                GPIO.output(self._ioPin, GPIO.LOW)

        except:
            print("Error or exception occurred!")
