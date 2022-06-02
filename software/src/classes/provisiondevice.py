# ==================================================================================
#   File:   provisiondevice.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Provisions Devices and updates cache file and do device provisioning
#           via DPS for IoT Central
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import time, logging, string, json, os, binascii, threading, datetime, pprint

# Our classes
import classes.constants as CONSTANTS
from classes.devicecache import DeviceCache
from classes.secrets import Secrets
from classes.symmetrickey import SymmetricKey
from classes.config import Config
from classes.printheader import PrintHeader
from classes.printerror import PrintError

# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import ProvisioningDeviceClient

# -------------------------------------------------------------------------------
#   ProvisionDevice Class
# -------------------------------------------------------------------------------
class ProvisionDevice:

    timer = None
    timer_ran = False
    dcm_value = None

    def __init__(self, Log, Verbose):

        # Initialization
        self._logger = Log
        self._verbose = Verbose
        self._module = "ProvisionDevice"

        # Load the configuration file
        self._config = Config(Log)
        self._config_cache_data = self._config.data

        # Tracing and Errors
        self._print_header = PrintHeader(Log, Verbose, self._config)
        self._print_error = PrintError(Log, Verbose, self._config)

        # Symmetric Key
        self._symmetrickey = SymmetricKey(Log, Verbose)

        # Secrets Cache
        self._secrets = None
        self._secrets_cache_data = []

        # Devices Cache
        self._device_cache = None
        self._device_cache_data = []

        # meta
        self._id_device = None
        self._application_uri = None
        self._namespace = None
        self._device_name = None
        self._device_default_component_id = None
        self._device_capability_model = []
        self._device_name_prefix = None
        self._ignore_interface_ids = []
        self._device_to_provision = None
        self._device_to_provision_array = []

    # -------------------------------------------------------------------------------
    #   Function:   provision_device
    #   Usage:      Grabs the Defined Devices and Provisions into IoT Central
    #               a provisioning call to associated a device template to the node
    #               interface based on the twin, device or gateway pattern
    # -------------------------------------------------------------------------------
    async def provision_device(self, Id):

        method = "provision_devices"

        # First up we gather all of the needed provisioning meta-data and secrets
        try:

            self._id_device = Id
            self._namespace = self._config_cache_data["Device"]["NameSpace"]
            self._device_default_component_id = self._config_cache_data["Device"][
                "Default Component Id"
            ]
            self._device_name_prefix = self._config_cache_data["Device"]["Device Name Prefix"]
            self._device_name = self._device_name_prefix.format(id=self._id_device)
            self._device_default_component_id = self._config_cache_data["Device"][
                "Default Component Id"
            ]

            # Load all our cache data
            self.load_caches()

            # this is our working device for things we provision in this session
            self._device_to_provision = self.create_device_to_provision()

            # __Verbose__
            self._print_header.print(self._module, method, self._device_to_provision, CONSTANTS.INFO)
            self._print_header.print(self._module, method, "DEVICE SYMMETRIC KEY %s"
            % (
                self._device_to_provision["Device"]["Secrets"]["DeviceSymmetricKey"],
            ), CONSTANTS.INFO)
            
            # Azure IoT Central SDK Call to create the provisioning_device_client
            provisioning_device_client = (
                ProvisioningDeviceClient.create_from_symmetric_key(
                    provisioning_host=self._secrets.provisioning_host,
                    registration_id=self._device_to_provision["Device"]["Name"],
                    id_scope=self._secrets.scope_id,
                    symmetric_key=self._device_to_provision["Device"]["Secrets"][
                        "DeviceSymmetricKey"
                    ],
                    websockets=True,
                )
            )

            # Azure IoT Central SDK call to set the payload and provision the device
            provisioning_device_client.provisioning_payload = '{"iotcModelId":"%s"}' % (
                self._device_to_provision["Device"]["Default Component Id"]
            )
            registration_result = await provisioning_device_client.register()

            # __Verbose__
            self._print_header.print(self._module, method, "RESULT: %s" % (registration_result), CONSTANTS.INFO)

            self._device_to_provision["Device"]["Secrets"][
                "AssignedHub"
            ] = registration_result.registration_state.assigned_hub

            # Add Capabilities/Interfaces
            # for node in self.config["Nodes"]:
            # self.device_to_provision["Device"]["Capabilities"].append(node["InterfaceInstanceName"])

            self._logger.info(self._device_to_provision)

            # Update Secrets Cache Data for Devices
            existing_device = [
                x
                for x in self._secrets_cache_data["Devices"]
                if x["Device"]["Name"] == self._device_to_provision["Device"]["Name"]
            ]

            self._logger.info("Here 3")

            if len(existing_device) == 0:
                self._secrets_cache_data["Devices"].append(self._device_to_provision)
            else:
                index = 0
                for device in self._secrets_cache_data["Devices"]:
                    if (
                        device["Device"]["Name"]
                        == self._device_to_provision["Device"]["Name"]
                    ):
                        self._secrets_cache_data["Devices"][index][
                            "Device"
                        ] = self._device_to_provision["Device"]
                        break
                    else:
                        index = index + 1

            # Update Full Device Information to the Secrets file.
            # IMPORTANT: This hides the secrets in file in .gitignore
            self._secrets.update_file_device_secrets(self._secrets_cache_data["Devices"])

            # Hide secrets from device cache file
            self._device_to_provision["Device"]["Secrets"] = None
            existing_device = [
                x
                for x in self._device_cache_data["Devices"]
                if x["Device"]["Name"] == self._device_to_provision["Device"]["Name"]
            ]
            
            if len(existing_device) == 0:
                self._device_cache_data["Devices"].append(self._device_to_provision)

            index = 0
            for device in self._device_cache_data["Devices"]:
                if (
                    device["Device"]["Name"]
                    == self._device_to_provision["Device"]["Name"]
                ):
                    self._device_cache_data["Devices"][index][
                        "Device"
                    ] = self._device_to_provision["Device"]
                    break
                else:
                    index = index + 1

            self._device_cache.update_file(self._device_cache_data)
            
            # __Verbose__
            self._print_header.print(self._module, method, "SUCCESS %s"
            % (
                self._device_to_provision
            ), CONSTANTS.INFO)

            return

        except Exception as ex:
            self._print_error.print(self._module, method, ex)

        return
        
    # -------------------------------------------------------------------------------
    #   Function:   create_device_to_provision`
    #   Usage:      Returns a Devices Array
    # -------------------------------------------------------------------------------
    def create_device_to_provision(self):
        method = "create_device_to_provision"
        try:

            # Get the node for the device we are provisioning
            newDeviceToProvision = {
                "Device": {
                    "Name": self._device_name,
                    "Default Component Id": self._device_default_component_id,
                    "LastProvisioned": str(datetime.datetime.now()),
                    "Secrets": {},
                }
            }

            # Get device symmetric key
            device_symmetric_key = self._symmetrickey.compute_derived_symmetric_key(
                self._device_name, self._secrets.device_secondary_key
            )

            # Get the Provisioned Device Secret
            newDeviceSecret = {
                "Name": self._device_name,
                "Default Component Id": self._device_default_component_id,
                "AssignedHub": "",
                "DeviceSymmetricKey": device_symmetric_key,
                "LastProvisioned": str(datetime.datetime.now()),
            }

            newDeviceToProvision["Device"]["Secrets"] = newDeviceSecret
        
            return newDeviceToProvision

        except Exception as ex:
            self._print_error.print(self._module, method, ex)

        return

    # -------------------------------------------------------------------------------
    #   Function:   create_device_capability_model
    #   Usage:      Returns a Device Interface with the  Interfaces Array
    # -------------------------------------------------------------------------------
    def create_device_capability_model(self):
        newDeviceCapabilityModel = {
            "Name": self._device_name,
            "Default Component Id": self._device_default_component_id,
            "LastProvisioned": str(datetime.datetime.now()),
        }

        return newDeviceCapabilityModel

    # -------------------------------------------------------------------------------
    #   Function:   create_device_interface
    #   Usage:      Returns a Device Interface for Interfaces Array
    # -------------------------------------------------------------------------------
    def create_device_interface(self, name, Id, instantName):
        newInterface = {
            "Name": name,
            "InterfacelId": Id,
            "InterfaceInstanceName": instantName,
        }

        return newInterface

    # -------------------------------------------------------------------------------
    #   Function:   load caches for provisioning
    #   Usage:      None
    # -------------------------------------------------------------------------------
    def load_caches(self):

        # Secrets Cache
        self._secrets = Secrets(self._logger, self._verbose)
        self._secrets_cache_data = self._secrets.data

        # Devices Cache
        self._device_cache = DeviceCache(self._logger)
        self._device_cache_data = self._device_cache.data

        return
