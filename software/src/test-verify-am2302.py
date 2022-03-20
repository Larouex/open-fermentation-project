# ==================================================================================
#   File:   test-verify-am2302.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Verifies that all Ambient Temerature and Humdity dependancies
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Software Design LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
import adafruit_dht, board
import logging as Log

# our classes
from classes.config import Config

# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

    # execution state from args
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
            print("HELP for test-verify-am2315.py")
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

        # setup pin to read
        pin = config["AmbientPin"]

        dhtDevice = adafruit_dht.DHT22(pin)

        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
