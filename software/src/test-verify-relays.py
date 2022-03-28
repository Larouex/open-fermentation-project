# ==================================================================================
#   File:   test-verify-relays.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Verify that the Relays are properly wired to the GPIO and cycling
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
import RPi.GPIO as GPIO
import logging as Log

# our classes
from classes.config import Config

GPIO.setmode(GPIO.BCM)

# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

    # execution state from args
    verbose = False
    short_options = "hvd"
    long_options = ["help", "verbose", "debug"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))

    for current_argument, current_value in arguments:

        if current_argument in ("-h", "--help"):
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            print("HELP for test-verify-relays.py")
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            print("")
            print("  BASIC PARAMETERS...")
            print("")
            print("  -h or --help - Print out this Help Information")
            print(
                "  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging"
            )
            print(
                "  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging"
            )
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            return

        if current_argument in ("-v", "--verbose"):
            verbose = True
            Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.INFO)
            Log.info("Verbose Logging Mode...")
        else:
            Log.basicConfig(format="%(levelname)s: %(message)s")

        if current_argument in ("-d", "--debug"):
            Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
            Log.info("Debug Logging Mode...")
        else:
            Log.basicConfig(format="%(levelname)s: %(message)s")

        # Load the configuration file
        logger = Log
        config = Config(logger)
        config = config.data

        # setup relays
        humidifier = config["Relays"]["Pins"]["Humidifier"]
        deHumidifier = config["Relays"]["Pins"]["DeHumidifier"]
        heater = config["Relays"]["Pins"]["Heater"]
        chiller = config["Relays"]["Pins"]["Chiller"]
        fan = config["Relays"]["Pins"]["Fan"]
        light = config["Relays"]["Pins"]["Light"]
        open1 = config["Relays"]["Pins"]["Open1"]
        open2 = config["Relays"]["Pins"]["Open2"]

        gpioList = {
            "Humidifier": humidifier,
            "DeHumidifier": deHumidifier,
            "Heater": heater,
            "Chiller": chiller,
            "Fan": fan,
            "Light": light,
            "Open1": open1,
            "Open2": open2,
        }

        # Print Relay Configuration Values
        if verbose == True:
            print("")
            print("-------------------------------------------------")
            print(" Assigned GPIO Pins for the Relays")
            print("-------------------------------------------------")
            for key in gpioList:
                print(key, ":", gpioList[key])

        # Print Relay Configuration Values
        GPIO.setwarnings(False)
        if verbose == True:
            print("")
            print("-------------------------------------------------")
            print(" Setting up the Relays GPIO State")
            print("-------------------------------------------------")
            for key in gpioList:
                GPIO.setup(gpioList[key], GPIO.OUT)
                GPIO.output(gpioList[key], GPIO.HIGH)
            print(" Completed")

        # Sleep time variables
        sleepTimeShort = 0.2
        sleepTimeLong = 0.1

        try:
            print("")
            print("-------------------------------------------------")
            print(" Toggle State of Each Relay in Loop...")
            print("-------------------------------------------------")
            while True:
                for key in gpioList:
                    print(key, ": (LOW)", gpioList[key])
                    GPIO.output(gpioList[key], GPIO.LOW)
                    time.sleep(sleepTimeShort)
                    print(key, ": (HIGH)", gpioList[key])
                    GPIO.output(gpioList[key], GPIO.HIGH)
                    time.sleep(sleepTimeLong)

        # End program cleanly with keyboard
        except KeyboardInterrupt:
            print("Exiting")

        # Reset GPIO settings
        GPIO.cleanup()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
