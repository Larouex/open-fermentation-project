# ==================================================================================
#   File:   deviceclient.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Azure IoT Central Device Client
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Software Design LLC
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

class DeviceClient():

    def __init__(self, Log, DeviceName):
      self.logger = Log

      # Azure Device
      self.device_name = DeviceName
      self.device_secrets = []
      self.device_client = None

    # -------------------------------------------------------------------------------
    #   Function:   connect
    #   Usage:      The connect function creates the device instance and connects
    # -------------------------------------------------------------------------------
    async def connect(self):

      try:

        # load the secrets
        secrets = Secrets(self.logger)
        secrets.init()
        self.device_secrets = secrets.get_device_secrets(self.device_name)
        print("here secrets")
        print(self.device_secrets)

        self.device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key = self.device_secrets["Device"]["Secrets"]["DeviceSymmetricKey"],
            hostname = self.device_secrets["Device"]["Secrets"]["AssignedHub"],
            device_id = self.device_name,
            websockets=True
        )
        await self.device_client.connect()
        self.logger.info("[DEVICE CLIENT] %s" % self.device_client)

      except Exception as ex:
        self.logger.error("[ERROR] %s" % ex)
        self.logger.error("[TERMINATING] We encountered an error creating and connecting the device in the Class::DeviceClient" )
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
      await self.device_client.send_message(msg)
      self.logger.info("[MESSAGE] %s" % msg)

    # -------------------------------------------------------------------------------
    #   Function:   disconnect
    #   Usage:      Disconnects from the IoT Hub
    # -------------------------------------------------------------------------------
    async def disconnect(self):
      self.device_client.disconnect()
      return
