# ==================================================================================
#   File:   symmetrickey.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    SaS key class for all operations on connections and generation of
#           keys used to connect via DPS and Azure IoT Central
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import base64, hmac, hashlib

import classes.constants as CONSTANTS
from classes.config import Config
from classes.printheader import PrintHeader
from classes.printerror import PrintError

class SymmetricKey:

    def __init__(self, Log, Verbose):

        # Initialization
        self._logger = Log
        self._verbose = Verbose
        self._module = "SymmetricKey"
        self._method = None

        # Load the configuration file
        self._config = Config(Log)

        # Tracing and Errors
        self._print_header = PrintHeader(Log, Verbose, self._config)
        self._print_error = PrintError(Log, Verbose, self._config)

        self.data = []

    # derives a symmetric device key for a device id
    # using the group symmetric key
    def compute_derived_symmetric_key(self, device_id, symmetric_key):

        self._method = "compute_derived_symmetric_key"

        try:

            message = device_id.encode("utf-8")
            signing_key = base64.b64decode(symmetric_key.encode("utf-8"))
            signed_hmac = hmac.HMAC(signing_key, message, hashlib.sha256)
            device_key_encoded = base64.b64encode(signed_hmac.digest())

            message = "Generated Device Key: {key}".format(key=str(device_key_encoded.decode("utf-8")))
            self._print_header.print(self._module, self._method, message, CONSTANTS.INFO)

            return device_key_encoded.decode("utf-8")
        
        except Exception as ex:
            self._print_error.print(self._module, self._method, ex)
