# ==================================================================================
#   File:   test-verify-env.py
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
    _verbose = True
    _module = "test-verify-env-dev.py"
    _method = "main()"

    # Tracing and Errors
    _print_header = PrintHeader(Log, _verbose)
    _print_error = PrintError(Log, _verbose)

    # __Verbose__
    _message = "Testing and Verifying the Environment..."
    _print_header.print(_module, _method, _message, CONSTANTS.INFO, False)

    # Load the configuration file
    _config = Config(Log, _verbose)
    _config_cache_data = _config.data

    # __Verbose__
    _message = "SUCCESS: Loaded the Configuration File (config.json)!"
    _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)
    if (_verbose == True):
        _message = "CONTENTS: {contents}".format(contents = _config_cache_data)
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)

    # Load the devicecache file
    _devicecache = DeviceCache(Log, _verbose)
    _devicecache_cache_data = _devicecache.data

    # __Verbose__
    _message = "SUCCESS: Loaded the Device Cache File (devicecache.json)!"
    _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)
    if (_verbose == True):
        _message = "CONTENTS: {contents}".format(contents = _devicecache_cache_data)
        _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)

    # Load the secrets file
    _secrets = Secrets(Log, _verbose)
    _secrets_cache_data = _secrets.data

    # __Verbose__
    _message = "SUCCESS: Loaded the Secrets File (secrets.json)!"
    _print_header.print(_module, _method, _message, CONSTANTS.INFO, True)
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

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
