# ==================================================================================
#   File:   opcua-server.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    OPC-UA Server Implementation for the Saluminator Hardware Raspberry Pi
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from classes.opcserver import OpcServer
from classes.config import Config
from classes.varianttype import VariantType

# -------------------------------------------------------------------------------
#   Start the OPC Server
# -------------------------------------------------------------------------------
async def start_server(WhatIf, CacheAddrSpace):

    # Start Server
    opc_server = OpcServer(Log, WhatIf, CacheAddrSpace)
    await opc_server.start()

    return


async def main(argv):

    whatif = False
    cache_addr_space = None

    # execution state from args
    short_options = "hvdwc:"
    long_options = ["help", "verbose", "debug", "whatif", "cacheaddrspace"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))

    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print("HELP for server.py")
            print(
                "------------------------------------------------------------------------------------------------------------------"
            )
            print("-h or --help - Print out this Help Information")
            print(
                "-v or --verbose - Verbose Mode with lots of INFO will be Output to Assist with Tracing and Debugging"
            )
            print(
                "-d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging"
            )
            print(
                "-w or --whatif - Combine with Verbose it will Output the Configuration sans starting the Server"
            )
            print("-c or --cacheaddrspace - Load or Dump")
            print(
                "------------------------------------------------------------------------------------------------------------------"
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

        if current_argument in ("-w", "--whatif"):
            whatif = True
            Log.info("Whatif Mode...")

        if current_argument in ("-c", "--cacheaddrspace"):
            cache_addr_space = current_value
            if cache_addr_space == "dump":
                Log.info("Cache Address Space Mode [DUMP]...")
            elif cache_addr_space == "load":
                Log.info("Cache Address Space Mode [LOAD]...")

    # Start Server
    await start_server(whatif, cache_addr_space)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
