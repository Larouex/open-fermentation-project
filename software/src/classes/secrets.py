# ==================================================================================
#   File:   secrets.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Loads the secrets file
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
from multiprocessing.spawn import is_forking
import time, logging, string, json

import classes.constants as CONSTANTS
from classes.printtracing import PrintTracing

# Azure IoT Libraries
from azure.keyvault.certificates import (
    CertificateClient,
    CertificatePolicy,
    CertificateContentType,
    WellKnownIssuerNames,
)
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys import KeyClient
from azure.identity import ClientSecretCredential


class Secrets:
    def __init__(self, Log):
        self._class = "Secrets"
        self._method = "__init__"

        try:

            # init
            self._filename = "secrets.json"
            self._logger = Log

            # Initiate the Secrets
            self._data = self.load_file()

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)

        return

    @property
    def data(self):
        return self._data

    # -------------------------------------------------------------------------------
    #   Function:   load_file
    #   Usage:      Load the Secrets.json file and execute __init()
    # -------------------------------------------------------------------------------
    def load_file(self):
        self._method = "load_file"

        try:
            with open(self._filename, "r") as config_file:
                return json.load(config_file)

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)

        return "[]"

    # -------------------------------------------------------------------------------
    #   Function:   update_file_device_secrets
    #   Usage:      Append the passed Devices Data to the Secrets.json
    # -------------------------------------------------------------------------------
    def update_file_device_secrets(self, data):
        self._method = "update_file_device_secrets"

        try:

            with open("secrets.json", "w") as configs_file:
                self._data["Devices"] = data
                configs_file.write(json.dumps(self._data, indent=2))

        except Exception as ex:
            self._logger.error("SECRETS:%s Error %s", ex, self._method)

        return

    # Propeties you can query
    @property
    def provisioning_host(self):
        return self._data["ProvisioningHost"]

    @property
    def ApplicationInsightsConnectionString(self):
        if self._data["UseKeyVault"]:
            return self._data["KeyVaultSecrets"]["ApplicationInsightsConnectionString"]
        else:
            return self._data["LocalSecrets"]["ApplicationInsightsConnectionString"]

    @property
    def scope_id(self):
        if self._data["UseKeyVault"]:
            return self._data["KeyVaultSecrets"]["ScopeId"]
        else:
            return self._data["LocalSecrets"]["ScopeId"]

    @property
    def device_primary_key(self):
        if self._data["UseKeyVault"]:
            return self._data["KeyVaultSecrets"]["DeviceConnect"]["SaSKeys"]["Primary"]
        else:
            return self._data["LocalSecrets"]["DeviceConnect"]["SaSKeys"]["Primary"]

    @property
    def device_secondary_key(self):
        if self._data["UseKeyVault"]:
            return self._data["KeyVaultSecrets"]["DeviceConnect"]["SaSKeys"][
                "Secondary"
            ]
        else:
            return self._data["LocalSecrets"]["DeviceConnect"]["SaSKeys"]["Secondary"]

    @property
    def gateway_primary_key(self):
        if self._data["UseKeyVault"]:
            return self._data["KeyVaultSecrets"]["GatewayConnect"]["SaSKeys"]["Primary"]
        else:
            return self._data["LocalSecrets"]["GatewayConnect"]["SaSKeys"]["Primary"]

    @property
    def gateway_secondary_key(self):
        if self._data["UseKeyVault"]:
            return self._data["KeyVaultSecrets"]["GatewayConnect"]["SaSKeys"][
                "Secondary"
            ]
        else:
            return self._data["LocalSecrets"]["GatewayConnect"]["SaSKeys"]["Secondary"]

    @property
    def devices_secrets_data(self):
        return self._data["Devices"]

    @property
    def device_secrets(self, DeviceName):
        return [x for x in self._data["Devices"] if x["Device"]["Name"] == DeviceName][
            0
        ]
