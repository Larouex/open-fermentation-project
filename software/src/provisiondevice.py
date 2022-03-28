# ==================================================================================
#   File:   provisiondevice.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Provision a Device in IoT Central
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from classes.provisiondevice import ProvisionDevice
from classes.config import Config

# -------------------------------------------------------------------------------
#   Provision Device
# -------------------------------------------------------------------------------
async def provision_device(Id, NumberOfDevices):

    provisiondevice = ProvisionDevice(Log)
    id = int(Id)
    await provisiondevice.provision_device(id)
    return True


async def main(argv):

    # defaults
    id = 1
    number_of_devices = 1

    # execution state from args
    short_options = "hvdr:n:"
    long_options = ["help", "verbose", "debug", "registerid=", "numberofdevices="]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))

    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):

            # Load the configuration file & get example of the
            # device name from the config file
            config = Config(Log)
            config = config.data
            device_name_prefix = config["Device"]["DeviceNamePrefix"]
            device_name_prefix = device_name_prefix.format(id=1)

            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            print("HELP for provisiondevices.py")
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
                "                         result in a device provisioned with the name: {}".format(
                    device_name_prefix
                )
            )
            print("       USAGE: -r 5")
            print("       DEFAULT: 1")
            print(
                "       NOTE: The Prefix for your devices is located in the config.json file ['Device']['DeviceNamePrefix']"
            )
            print("")
            print(
                "    -n or --numberofdevices - The value is used to enumerate and provision the device(s) count specified."
            )
            print(
                "                              NOTE: LIMIT OF 10 DEVICES PER SESSION. You can run the provisiondevices.py via"
            )
            print(
                "                              a script and indicate --registerid with the sequential numbering if you want to"
            )
            print("                              provision more devices.")
            print("       USAGE: -n 10")
            print("       DEFAULT: 1")
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

        if current_argument in ("-r", "--registerid"):
            id = current_value
            Log.info("Register Id is Specified as: {id}".format(id=id))

            # validate the number is a NUMBER
            if id.isnumeric() == False:
                print("[ERROR] -r --registerid must be a numeric value")
                return

        if current_argument in ("-n", "--numberofdevices"):
            number_of_devices = current_value
            Log.info(
                "Number of Devices is Specified as: {numberofdevices}".format(
                    numberofdevices=number_of_devices
                )
            )

            # validate the number is a NUMBER
            if isinstance(number_of_devices, str) and not number_of_devices.isnumeric():
                print(
                    "[ERROR] -n --numberofdevices must be a numeric value between 1 and 10"
                )
                return
            elif isinstance(number_of_devices, str):
                number_of_devices = int(number_of_devices)

            # validate the number is contrained to our boundary
            if number_of_devices > 10:
                print(
                    "[ERROR] -n --numberofdevices must be a numeric value between 1 and 10"
                )
                return

    await provision_device(id, number_of_devices)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
