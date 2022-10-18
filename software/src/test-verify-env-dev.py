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
import argparse, sys, time, string, threading, asyncio, os
import logging as Log

# Our classes
from classes.devicecache import DeviceCache
from classes.secrets import Secrets
from classes.recipes import Recipes
from classes.symmetrickey import SymmetricKey
import classes.constants as CONSTANTS
from classes.printtracing import PrintTracing
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
    _parser = argparse.ArgumentParser()
    _parser.add_argument("-v", "--verbose", dest='verbose', action="store_true", help="Output Important information when executing.")
    _parser.add_argument("-d", "--debug", dest='debug', action="store_true", help="Output Debug information when executing.")
    args = _parser.parse_args()

    # gather parameters
    _verbose = args.verbose
    _debug = args.debug

    if _verbose:
        Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.INFO)
        Log.info("Verbose Logging Mode...")
    else:
        Log.basicConfig(format="%(levelname)s: %(message)s")

    if _debug:
        Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
        Log.info("Debug Logging Mode...")
    else:
        Log.basicConfig(format="%(levelname)s: %(message)s")


    # Load the configuration file
    _config = Config(Log)

    # Tracing and Errors
    _printtracing = PrintTracing(Log, _verbose, _config)
    _printtracing.printheader(_module, _method)
    _message = "Testing and Verifying the Environment..."
    _printtracing.forceprint(_message)

    # __Verbose__
    _message = "(Config) SUCCESS: Loaded the Configuration File (config.json)"
    _printtracing.forceprint(_message)
    if (_verbose == True):
        _message = "(Config) CONTENTS: {contents}".format(contents = _config.data)
        _printtracing.forceprint(_message)

    # Load the devicecache file
    _devicecache = DeviceCache(Log)

    # __Verbose__
    _message = "(DeviceCache) SUCCESS: Loaded the Device Cache File (devicecache.json)"
    _printtracing.forceprint(_message)
    if (_verbose == True):
        _message = "(DeviceCache) CONTENTS: {contents}".format(contents = _devicecache.data)
        _printtracing.forceprint(_message)

    # Load the secrets file
    _secrets = Secrets(Log)

    # __Verbose__
    _message = "(Secrets) SUCCESS: Loaded the Secrets File (secrets.json)"
    _printtracing.forceprint(_message)
    if (_verbose == True):
        _message = "(Secrets) PROVISIONING HOST: {contents}".format(contents = _secrets.provisioning_host)
        _printtracing.forceprint(_message)
        _message = "(Secrets) SCOPE ID: {contents}".format(contents = _secrets.scope_id)
        _printtracing.forceprint(_message)
        _message = "(Secrets) DEVICE PRIMARY KEY: {contents}".format(contents = _secrets.device_primary_key)
        _printtracing.forceprint(_message)
        _message = "(Secrets) DEVICE SECONDARY KEY: {contents}".format(contents = _secrets.device_secondary_key)
        _printtracing.forceprint(_message)
        _message = "(Secrets) GATEWAY PRIMARY KEY: {contents}".format(contents = _secrets.gateway_primary_key)
        _printtracing.forceprint(_message)
        _message = "(Secrets) GATEWAY SECONDARY KEY: {contents}".format(contents = _secrets.gateway_secondary_key)
        _printtracing.forceprint(_message)

    # Load the recipes file
    _recipes = Recipes(Log)

    # __Verbose__
    _message = "(Recipes) SUCCESS: Loaded the Recipes File (recipes.json)"
    _printtracing.forceprint(_message)
    if (_verbose == True):
        _message = "(Recipes) CONTENTS: {contents}".format(contents = _recipes.data)
        _printtracing.forceprint(_message)

    return
    
if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
