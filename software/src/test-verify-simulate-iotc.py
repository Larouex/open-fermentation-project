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
from classes.deviceclient import DeviceClient

# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

    # Load the configuration file
    logger = Log
    config = Config(logger)

    # defaults
    id = 1
    verbose = False

    # Load the configuration file & get example of the
    # device name from the config file
    device_name_prefix = config.data["Device"]["Device Name Prefix"]
    device_name = device_name_prefix.format(id=id)

    # execution state from args
    short_options = "hvdr:"
    long_options = ["help", "verbose", "debug", "registerid="]
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
            print("")
            print("  OPTIONAL PARAMETERS...")
            print("")
            print(
                "    -r or --registerid - This numeric value will get appended to your provisioned device. Example '1' would"
            )
            print(
                "                         result in a device provisioned with the name: {}".format(device_name)
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
       
        if current_argument in ("-r", "--registerid"):
            id = current_value
            Log.info("Register Id is Specified as: {id}".format(id=id))

            # validate the number is a NUMBER
            if id.isnumeric() == False:
                print("[ERROR] -r --registerid must be a numeric value")
                return
            
            # update if needed
            device_name = device_name_prefix.format(id=id)


        # Load Simulation
        simulate = Simulate(Log, verbose, config)

        # create our IoT Central Device Client
        device_client = DeviceClient(Log, device_name)
        await device_client.connect()

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

            # Payload
            payload =  '{{"ambient_temperature": {:.2f},"ambient_humidity": {:},"chamber_temperature": {:.2f},"chamber_humidity": {:}}}'
            print("PAYLOAD: " + payload.format(simulate.ambient_temperature, simulate.ambient_humdity, simulate.chamber_temperature, simulate.chamber_humdity))
            await device_client.send_telemetry(payload, "", "")
            print(
                "...SLEEPING FOR...{:} Seconds".format(
                    config.data["Simulation"]["Loop Delay"]
                )
            )
            time.sleep(int(config.data["Simulation"]["Loop Delay"]))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
