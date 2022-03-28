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
from classes.devicecache import DeviceCache
from classes.secrets import Secrets
from classes.symmetrickey import SymmetricKey
from classes.config import Config

# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import ProvisioningDeviceClient

# -------------------------------------------------------------------------------
#   ProvisionDevice Class
# -------------------------------------------------------------------------------
class ProvisionDevice:

    timer = None
    timer_ran = False
    dcm_value = None

    def __init__(self, Log):

        # Initialization
        self.logger = Log
        self.id_device = None

        # Load the configuration file
        self.config = Config(self.logger)
        self.config = self.config.data

        # Logging Mappers
        data = [
            x for x in self.config["ClassLoggingMaps"] if x["Name"] == "ProvisionDevice"
        ]
        self.class_name_map = data[0]["LoggingId"]

        # Symmetric Key
        self.symmetrickey = SymmetricKey(self.logger)

        # Secrets Cache
        self.secrets = None
        self.secrets_cache_data = []

        # Devices Cache
        self.devices_cache = None
        self.devices_cache_data = []

        # meta
        self.application_uri = None
        self.namespace = None
        self.device_name = None
        self.device_default_component_id = None
        self.device_capability_model = []
        self.device_name_prefix = None
        self.ignore_interface_ids = []
        self.device_to_provision = None
        self.device_to_provision_array = []

    # -------------------------------------------------------------------------------
    #   Function:   provision_devices
    #   Usage:      Grabs the Defined Devices and Provisions into IoT Central
    #               a provisioning call to associated a device template to the node
    #               interface based on the twin, device or gateway pattern
    # -------------------------------------------------------------------------------
    async def provision_devices(self, Id):

        # First up we gather all of the needed provisioning meta-data and secrets
        try:

            self.id_device = Id
            self.namespace = self.config["Device"]["NameSpace"]
            self.device_default_component_id = self.config["Device"][
                "DefaultComponentId"
            ]
            self.device_name_prefix = self.config["Device"]["DeviceNamePrefix"]
            self.device_name = self.device_name_prefix.format(id=self.id_device)
            self.device_default_component_id = self.config["Device"][
                "DefaultComponentId"
            ]

            # Load all our cache data
            self.load_caches()

            # this is our working device for things we provision in this session
            self.device_to_provision = self.create_device_to_provision()

            self.logger.info("************************************************")
            self.logger.info("[%s] DEVICE TO PROVISION" % self.class_name_map)
            self.logger.info(pprint.pformat(self.device_to_provision))
            self.logger.info("************************************************")

            # Azure IoT Central SDK Call to create the provisioning_device_client
            provisioning_device_client = (
                ProvisioningDeviceClient.create_from_symmetric_key(
                    provisioning_host=self.secrets.get_provisioning_host(),
                    registration_id=self.device_to_provision["Device"]["Name"],
                    id_scope=self.secrets.get_scope_id(),
                    symmetric_key=self.device_to_provision["Device"]["Secrets"][
                        "DeviceSymmetricKey"
                    ],
                    websockets=True,
                )
            )

            # Azure IoT Central SDK call to set the payload and provision the device
            provisioning_device_client.provisioning_payload = '{"iotcModelId":"%s"}' % (
                self.device_to_provision["Device"]["DefaultComponentId"]
            )
            registration_result = await provisioning_device_client.register()
            self.logger.info(
                "[%s] RESULT %s" % (self.class_name_map, registration_result)
            )
            self.logger.info(
                "[%s] DEVICE SYMMETRIC KEY %s"
                % (
                    self.class_name_map,
                    self.device_to_provision["Device"]["Secrets"]["DeviceSymmetricKey"],
                )
            )
            self.device_to_provision["Device"]["Secrets"][
                "AssignedHub"
            ] = registration_result.registration_state.assigned_hub

            # Add Capabilities/Interfaces
            # for node in self.config["Nodes"]:
            # self.device_to_provision["Device"]["Capabilities"].append(node["InterfaceInstanceName"])

            # Update Secrets Cache Data for Devices
            existing_device = [
                x
                for x in self.secrets_cache_data["Devices"]
                if x["Device"]["Name"] == self.device_to_provision["Device"]["Name"]
            ]

            if len(existing_device) == 0:
                self.secrets_cache_data["Devices"].append(self.device_to_provision)
            else:
                index = 0
                for device in self.secrets_cache_data["Devices"]:
                    if (
                        device["Device"]["Name"]
                        == self.device_to_provision["Device"]["Name"]
                    ):
                        self.secrets_cache_data["Devices"][index][
                            "Device"
                        ] = self.device_to_provision["Device"]
                        break
                    else:
                        index = index + 1

            # Update Full Device Information to the Secrets file.
            # IMPORTANT: This hides the secrets in file in .gitignore
            self.secrets.update_file_device_secrets(self.secrets_cache_data["Devices"])

            # Hide secrets from device cache file
            self.device_to_provision["Device"]["Secrets"] = None
            existing_device = [
                x
                for x in self.devices_cache_data["Devices"]
                if x["Device"]["Name"] == self.device_to_provision["Device"]["Name"]
            ]
            if len(existing_device) == 0:
                self.devices_cache_data["Devices"].append(self.device_to_provision)

            index = 0
            for device in self.devices_cache_data["Devices"]:
                if (
                    device["Device"]["Name"]
                    == self.device_to_provision["Device"]["Name"]
                ):
                    self.devices_cache_data["Devices"][index][
                        "Device"
                    ] = self.device_to_provision["Device"]
                    break
                else:
                    index = index + 1

            self.devices_cache.update_file(self.devices_cache_data)

            self.logger.info("************************************************")
            self.logger.info("[%s] SUCCESS:" % self.class_name_map)
            self.logger.info(pprint.pformat(self.device_to_provision))
            self.logger.info("************************************************")

            return

        except Exception as ex:
            self.logger.error("[ERROR] %s" % ex)
            self.logger.error(
                "[TERMINATING] We encountered an error in provision_devices()"
            )

    # -------------------------------------------------------------------------------
    #   Function:   create_device_to_provision`
    #   Usage:      Returns a Devices Array
    # -------------------------------------------------------------------------------
    def create_device_to_provision(self):

        newDeviceToProvision = {
            "Device": {
                "Name": self.device_name,
                "DefaultComponentId": self.device_default_component_id,
                "LastProvisioned": str(datetime.datetime.now()),
                "Secrets": {},
            }
        }
        print(self.secrets.get_device_primary_key())

        # Get device symmetric key
        device_symmetric_key = self.symmetrickey.compute_derived_symmetric_key(
            self.device_name, self.secrets.get_device_secondary_key()
        )

        newDeviceSecret = {
            "Name": self.device_name,
            "DefaultComponentId": self.device_default_component_id,
            "AssignedHub": "",
            "DeviceSymmetricKey": device_symmetric_key,
            "LastProvisioned": str(datetime.datetime.now()),
        }

        newDeviceToProvision["Device"]["Secrets"] = newDeviceSecret

        return newDeviceToProvision

    # -------------------------------------------------------------------------------
    #   Function:   create_device_capability_model
    #   Usage:      Returns a Device Interface with the  Interfaces Array
    # -------------------------------------------------------------------------------
    def create_device_capability_model(self):
        newDeviceCapabilityModel = {
            "Name": self.device_name,
            "DefaultComponentId": self.device_default_component_id,
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
        self.secrets = Secrets(self.logger)
        self.secrets_cache_data = self.secrets.data

        # Devices Cache
        self.devices_cache = DevicesCache(self.logger)
        self.devices_cache_data = self.devices_cache.data

        return
