# ==================================================================================
#   File:   deviceclient.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Azure IoT Central Device Client
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, sys, time, string, threading, asyncio, os, copy
import logging

# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from azure.iot.device import MethodResponse

# our classes
from classes.secrets import Secrets


class DeviceClient:
    def __init__(self, Log, DeviceName):
        self._logger = Log

        # Azure Device
        self._device_name = DeviceName
        self._device_secrets = []
        self._device_client = None

        self._device_symmetric_key = None
        self._assigned_hub = None

        # load the secrets
        secrets = Secrets(self._logger)

        # Get the needed device secrets
        for x in secrets.data["Devices"]:
            if x["Device"]["Name"] == self._device_name:
                self._device_symmetric_key = x["Device"]["Secrets"]["DeviceSymmetricKey"]
                self._logger.info("[DeviceSymmetricKey] %s" % self._device_symmetric_key)
                self._assigned_hub = x["Device"]["Secrets"]["AssignedHub"]
                self._logger.info("[AssignedHub] %s" % self._assigned_hub)

    # -------------------------------------------------------------------------------
    #   Function:   connect
    #   Usage:      The connect function creates the device instance and connects
    # -------------------------------------------------------------------------------
    async def connect(self):

        try:

            self._device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=self._device_symmetric_key,
                hostname=self._assigned_hub,
                device_id=self._device_name,
                websockets=True,
            )
            await self._device_client.connect()
            self._logger.info("[DEVICE CLIENT] %s" % self._device_client)

        except Exception as ex:
            self._logger.error("[ERROR] %s" % ex)
            self._logger.error(
                "[TERMINATING] We encountered an error creating and connecting the device in the Class::DeviceClient"
            )
            return None

        return

    # -------------------------------------------------------------------------------
    #   Function:   send_telemetry
    #   Usage:      Loads the Map Telemetry File that Maps Telemtry for Azure
    #               Iot Central to the Node Id's for the Opc Server.
    # -------------------------------------------------------------------------------
    async def send_telemetry(self, Telemetry, InterfacelId, InterfaceInstanceName):
        msg = Message(json.dumps(Telemetry))
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        msg.custom_properties["$.ifname"] = InterfaceInstanceName
        msg.custom_properties["$.ifid"] = InterfacelId
        await self._device_client.send_message(msg)
        self._logger.info("[MESSAGE] %s" % msg)

    # -------------------------------------------------------------------------------
    #   Function:   disconnect
    #   Usage:      Disconnects from the IoT Hub
    # -------------------------------------------------------------------------------
    async def disconnect(self):
        self._device_client.disconnect()
        return
