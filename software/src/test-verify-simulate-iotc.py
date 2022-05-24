# ==================================================================================
#   File:   test-verify-simulate-iotc.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Verifies the connection to IoT Central and sends Telemetry
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from classes.config import Config
from classes.simulate import Simulate

# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

    # execution state from args
    short_options = "hvd"
    long_options = ["help", "verbose", "debug"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    verbose= False

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))

    for current_argument, current_value in arguments:

        if current_argument in ("-h", "--help"):
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            print("HELP for test-verify-simulate-iotc.py")
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
            verbose = True
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
        
        # Load Simulation
        simulate = Simulate(Log, verbose, config)

        while True:
            simulate.RunSimulation()

            # Print the simulated values to the serial port
            print(
                "AMBIENT: Temp: [{:.1f}] F Humidity: {:} Rh% ".format(
                    simulate.ambient_temperature, simulate.ambient_humdity
                )
            )
            print(
                "CHAMBER: Temp: [{:.1f}] F Humidity: {:} Rh% ".format(
                    simulate.chamber_temperature, simulate.chamber_humdity
                )
            )
            print(
                "...SLEEPING FOR...{:} Seconds".format(
                    config.data["Simulation"]["Loop Delay"]
                )
            )
            time.sleep(int(config.data["Simulation"]["Loop Delay"]))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
