# ==================================================================================
#   File:   test-verify-env-dev.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Verify that the Environment and Dependancies are all working...
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
import logging as Log

# Our classes
from classes.devicecache import DeviceCache
from classes.secrets import Secrets
from classes.recipes import Recipes
from classes.symmetrickey import SymmetricKey
import classes.constants as CONSTANTS
from classes.printheader import PrintHeader
from classes.printerror import PrintError
from classes.config import Config

# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

    # Initialization
    _verbose = False
    _module = "test-verify-env-dev.py"
    _method = "main()"

    # execution state from args
    short_options = "hvd"
    long_options = ["help", "verbose", "debug"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    arguments, values = getopt.getopt(argument_list, short_options, long_options)

    for current_argument, current_value in arguments:

        if current_argument in ("-h", "--help"):
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            print("HELP for test-verify-env-dev.py")
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
            _verbose = True
            Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.INFO)
            Log.info("Verbose Logging Mode...")
        else:
            Log.basicConfig(format="%(levelname)s: %(message)s")

        if current_argument in ("-d", "--debug"):
            Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
            Log.info("Debug Logging Mode...")
        else:
            Log.basicConfig(format="%(levelname)s: %(message)s")


    # Tracing and Errors
    _print_header = PrintHeader(Log, _verbose)
    _print_error = PrintError(Log, _verbose)

    # __Verbose__
    _message = "Testing and Verifying the Environment..."
    _print_header.forceprint(_module, _method, _message, CONSTANTS.INFO, False)

    # Load the configuration file
    _config = Config(Log, _verbose)
    _config_cache_data = _config.data

    # __Verbose__
    _message = "SUCCESS: Loaded the Configuration File (config.json)!"
    _print_header.forceprint(_module, _method, _message, CONSTANTS.INFO, True)
    if (_verbose == True):
        _message = "CONTENTS: {contents}".format(contents = _config_cache_data)
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)

    # Load the devicecache file
    _devicecache = DeviceCache(Log, _verbose)
    _devicecache_cache_data = _devicecache.data

    # __Verbose__
    _message = "SUCCESS: Loaded the Device Cache File (devicecache.json)!"
    _print_header.forceprint(_module, _method, _message, CONSTANTS.INFO, True)
    if (_verbose == True):
        _message = "CONTENTS: {contents}".format(contents = _devicecache_cache_data)
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)

    # Load the secrets file
    _secrets = Secrets(Log, _verbose)
    _secrets_cache_data = _secrets.data

    # __Verbose__
    _message = "SUCCESS: Loaded the Secrets File (secrets.json)!"
    _print_header.forceprint(_module, _method, _message, CONSTANTS.INFO, True)
    if (_verbose == True):
        _message = "(Secrets) PROVISIONING HOST: {contents}".format(contents = _secrets.get_provisioning_host())
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)
        _message = "(Secrets) SCOPE ID: {contents}".format(contents = _secrets.get_scope_id())
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)
        _message = "(Secrets) DEVICE PRIMARY KEY: {contents}".format(contents = _secrets.get_device_primary_key())
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)
        _message = "(Secrets) DEVICE SECONDARY KEY: {contents}".format(contents = _secrets.get_device_secondary_key())
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)
        _message = "(Secrets) GATEWAY PRIMARY KEY: {contents}".format(contents = _secrets.get_gateway_primary_key())
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)
        _message = "(Secrets) GATEWAY SECONDARY KEY: {contents}".format(contents = _secrets.get_gateway_secondary_key())
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)

    # Load the recipes file
    _recipes = Recipes(Log, _verbose)
    _recipes_cache_data = _recipes.data

    # __Verbose__
    _message = "SUCCESS: Loaded the Recipes File (recipes.json)!"
    _print_header.forceprint(_module, _method, _message, CONSTANTS.INFO, True)
    if (_verbose == True):
        _message = "CONTENTS: {contents}".format(contents = _recipes_cache_data)
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
