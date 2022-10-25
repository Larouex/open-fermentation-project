# ==================================================================================
#   File:   opcserver.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    This is the class that handles config and creation of the OPC Server
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, sys, time, string, threading, asyncio, os, copy
import logging

# For dumping and Loading Address Space option
from pathlib import Path

# opcua
from asyncua import ua, Server
from asyncua.common.methods import uamethod

# our classes
from classes.config import Config
from classes.maptelemetry import MapTelemetry
from classes.varianttype import VariantType

# open telemetry
from classes.otelmetering import OtelMetering

class OpcuaServer:
    def __init__(self, Log, WhatIf, CacheAddrSpace):
        self.logger = Log
        self.whatif = WhatIf
        self.cache_addr_space = CacheAddrSpace
        self.config = []
        self.nodes = []
        self.nodes_dict = {}
        self.nodes_dict_counter = {}
        self.map_telemetry = []
        self.map_telemetry_nodes = []
        self.map_telemetry_nodes_variables = []
        self.load_config()

    # -------------------------------------------------------------------------------
    #   Function:   start
    #   Usage:      The start function loads configuration and starts the OPC Server
    # -------------------------------------------------------------------------------
    async def start(self):

        node_obj = {}
        variable_obj = {}

        # Data Type Mappings (OPCUA Datatypes to IoT Central Datatypes)
        variant_type = VariantType(self.logger)

        # OPCUA Server Setup
        # Here we setup the Server and add discovery
        try:

            # configure the endpoint
            opc_url = self.config["ServerUrlPattern"].format(
                ip=self.config["IPAddress"], port=self.config["Port"]
            )

            if not self.whatif:

                # init the server
                opc_server = Server()
                await opc_server.init()

                # set the endpoint and name
                opc_server.set_endpoint(opc_url)
                opc_server.set_server_name(self.config["ServerDiscoveryName"])

                # set discovery
                await opc_server.set_application_uri(self.config["ApplicationUri"])

            log_msg = "[SERVER CONFIG] ENDPOINT: {ep} APPLICATION URI: {au} APPLICATION NAME: {an}"
            self.logger.info(
                log_msg.format(
                    ep=opc_url,
                    au=self.config["ApplicationUri"],
                    an=self.config["ServerDiscoveryName"],
                )
            )

            # Setup root for Map Telemetry
            self.map_telemetry = self.create_map_telemetry(
                self.config["NameSpace"], self.config["DeviceCapabilityModelId"]
            )

        except Exception as ex:
            self.logger.error("[ERROR] %s" % ex)
            self.logger.error(
                "[TERMINATING] We encountered an error in OPCUA Server Setup"
            )
            return

        # OPCUA Server Setup Nodes
        # Here we setup the Nodes and Variables
        try:

            # Set NameSpace
            namespace = self.config["NameSpace"]
            self.logger.info("[NAMESPACE] %s" % namespace)

            if not self.whatif:
                id_namespace = await opc_server.register_namespace(namespace)

            node_count = 0

            # Create our Nodes and Parameters
            for node in self.nodes:

                # Add Node and Begin Populating our Address Space
                if not self.whatif:

                    # Create Node
                    node_obj[node["Name"]] = await opc_server.nodes.objects.add_object(
                        id_namespace, node["Name"]
                    )
                    self.logger.info("[NODE ID] %s" % node_obj[node["Name"]])

                    # Setup nodes for Map Telemetry
                    self.map_telemetry["Nodes"].append(
                        self.create_map_telemetry_node(
                            node["Name"],
                            str(node_obj[node["Name"]]),
                            node["InterfacelId"],
                            node["InterfaceInstanceName"],
                        )
                    )

                for variable in node["Variables"]:

                    variable_name = variable["DisplayName"]
                    telemetry_name = variable["TelemetryName"]
                    range_value = variable["SimulationRangeValues"][0]
                    opc_variant_type = variant_type.map_variant_type(
                        variable["IoTCDataType"]
                    )
                    log_msg = (
                        "[SETUP VARIABLE] NODE NAME: {nn} DISPLAY NAME: {dn} TELEMETRY NAME: {tn} RANGE VALUE: {rv} "
                        "IoTC TYPE: {it} OPC VARIANT TYPE {ovt} OPC DATA TYPE {odt}"
                    )
                    self.logger.info(
                        log_msg.format(
                            nn=node["Name"],
                            dn=variable["DisplayName"],
                            vn=variable["TelemetryName"],
                            tn=variable["TelemetryName"],
                            rv=variable["SimulationRangeValues"][0],
                            it=variable["IoTCDataType"],
                            ovt=opc_variant_type,
                            odt=opc_variant_type,
                        )
                    )

                    if not self.whatif:

                        # Create Node Variable
                        nodeObject = await node_obj[node["Name"]].add_variable(
                            id_namespace, telemetry_name, range_value
                        )
                        await nodeObject.set_writable()
                        variable_obj[telemetry_name] = nodeObject
                        self.map_telemetry_nodes_variables.append(
                            self.create_map_telemetry_variable(
                                variable_name,
                                telemetry_name,
                                str(variable_obj[telemetry_name]),
                                variable["IoTCDataType"],
                            )
                        )

                if not self.whatif:
                    self.map_telemetry["Nodes"][node_count]["Variables"] = copy.copy(
                        self.map_telemetry_nodes_variables
                    )
                    self.logger.info("[MAP] %s" % self.map_telemetry)
                    self.map_telemetry_nodes_variables = []

                node_count += 1

            if not self.whatif:
                self.update_map_telemetry()

        except Exception as ex:
            self.logger.error("[ERROR] %s" % ex)
            self.logger.error(
                "[TERMINATING] We encountered an error in OPCUA Server Setup for the Nodes and Variables"
            )
            return

        # Start the server and save the address space
        try:

            if not self.whatif and self.cache_addr_space == "save":
                filename = Path(self.config["CacheAddrSpaceFileName"])
                opc_server.start()
                opc_server.iserver.dump_address_space(filename)
                opc_server.stop()
                self.logger.info(
                    "[CACHE ADDRESS SPACE] Saved and Server Terminated. Now run with -c load"
                )
                return

        except Exception as ex:
            self.logger.error("[ERROR] %s" % ex)
            self.logger.error(
                "[TERMINATING] We encountered an error in OPCUA Server Setup for the Nodes and Variables"
            )
            return

        # We start the server loop if we are not in WhatIf and the CacheAddrSpace
        # is null (not set) or load. If it was load, we pulled it from the cache on
        # server init()...
        if not self.whatif and (
            self.cache_addr_space == None or self.cache_addr_space == "load"
        ):

            self.logger.info("[STARTING SERVER] %s" % opc_url)

            if self.cache_addr_space == "load":
                filename = Path(self.config["CacheAddrSpaceFileName"])
                opc_server.iserver.load_address_space(filename)
                self.logger.info(
                    "[CACHE ADDRESS SPACE] Loaded Address Space Cache from %s"
                    % filename
                )

            opc_server.start()

            async with opc_server:
                while True:
                    for node in self.nodes:
                        temp_dict = self.nodes_dict[node["Name"]]
                        temp_dict_counter = self.nodes_dict_counter[node["Name"]]

                        for variable in node["Variables"]:
                            count = temp_dict_counter[variable["TelemetryName"]]
                            sequence_count = temp_dict[variable["TelemetryName"]]

                            if count > (sequence_count - 1):
                                count = 0

                            # Choose the next value in the telemetry sequence for the variable
                            self.nodes_dict_counter[node["Name"]][
                                variable["TelemetryName"]
                            ] = (count + 1)
                            value = variable["SimulationRangeValues"][count]

                            if not self.whatif:
                                await variable_obj[
                                    variable["TelemetryName"]
                                ].write_value(value)

                            log_msg = "[LOOP] {nn} {tn} {vw} {tc} SEQ({sc}) CUR({cc})"
                            self.logger.info(
                                log_msg.format(
                                    nn=node["Name"],
                                    tn=variable["TelemetryName"],
                                    vw=value,
                                    tc=count,
                                    sc=temp_dict[variable["TelemetryName"]],
                                    cc=temp_dict_counter[variable["TelemetryName"]],
                                )
                            )
                    self.logger.info("Pausing for %s seconds..." % self.config["ServerFrequencyInSeconds"])
                    time.sleep(self.config["ServerFrequencyInSeconds"])

        else:

            while True:
                for node in self.nodes:
                    temp_dict = self.nodes_dict[node["Name"]]
                    temp_dict_counter = self.nodes_dict_counter[node["Name"]]

                    for variable in node["Variables"]:
                        count = temp_dict_counter[variable["TelemetryName"]]
                        sequence_count = temp_dict[variable["TelemetryName"]]

                        if count > (sequence_count - 1):
                            count = 0

                        # Choose the next value in the telemetry sequence for the variable
                        self.nodes_dict_counter[node["Name"]][
                            variable["TelemetryName"]
                        ] = (count + 1)
                        value = variable["SimulationRangeValues"][count]
                        log_msg = "[LOOP] {nn} {tn} {vw} {tc} SEQ({sc}) CUR({cc})"
                        self.logger.info(
                            log_msg.format(
                                nn=node["Name"],
                                tn=variable["TelemetryName"],
                                vw=value,
                                tc=count,
                                sc=temp_dict[variable["TelemetryName"]],
                                cc=temp_dict_counter[variable["TelemetryName"]],
                            )
                        )
                self.logger.info("Pausing for %s seconds..." % self.config["ServerFrequencyInSeconds"])
                time.sleep(self.config["ServerFrequencyInSeconds"])

        return

    # -------------------------------------------------------------------------------
    #   Function:   load_config
    #   Usage:      Loads the configuration from file and setup iterators for
    #               sending telemetry in sequence
    # -------------------------------------------------------------------------------
    def load_config(self):

        # Load all the configuration
        config = Config(self.logger)
        self.config = config.data
        self.nodes = self.config["Nodes"]

        # These counters support looping through our bounded telemetry values
        for node in self.nodes:
            variable_dict = {}
            variable_dict_counter = {}
            for variable in node["Variables"]:
                variable_dict[variable["TelemetryName"]] = len(
                    variable["SimulationRangeValues"]
                )
                variable_dict_counter[variable["TelemetryName"]] = 0

            self.nodes_dict[node["Name"]] = copy.deepcopy(variable_dict)
            self.nodes_dict_counter[node["Name"]] = copy.copy(variable_dict_counter)
            log_msg = "[LOOP DICTIONARY] NAME: {n} COUNTER: {c}"
            self.logger.info(
                log_msg.format(
                    n=self.nodes_dict[node["Name"]],
                    c=self.nodes_dict_counter[node["Name"]],
                )
            )

        self.logger.info("[NODES_DICT] %s" % self.nodes_dict)
        self.logger.info("[NODES_DICT_COUNTER] %s" % self.nodes_dict_counter)

    # -------------------------------------------------------------------------------
    #   Function:   create_map_telemetry
    #   Usage:      Sets the root for the Map Telemetry configuration file
    # -------------------------------------------------------------------------------
    def create_map_telemetry(self, NameSpace, DeviceCapabilityModelId):
        mapTelemetry = {
            "NameSpace": NameSpace,
            "DeviceCapabilityModelId": DeviceCapabilityModelId,
            "Nodes": [],
        }
        return mapTelemetry

    # -------------------------------------------------------------------------------
    #   Function:   create_map_telemetry_node
    #   Usage:      Sets the node for the Map Telemetry configuration file
    # -------------------------------------------------------------------------------
    def create_map_telemetry_node(
        self, Name, NodeId, InterfacelId, InterfaceInstanceName
    ):
        mapTelemetryNode = {
            "Name": Name,
            "NodeId": NodeId,
            "InterfacelId": InterfacelId,
            "InterfaceInstanceName": InterfaceInstanceName,
            "Variables": [],
        }
        return mapTelemetryNode

    # -------------------------------------------------------------------------------
    #   Function:   create_map_telemetry_variable
    #   Usage:      Sets the variable for the Map Telemetry configuration file
    # -------------------------------------------------------------------------------
    def create_map_telemetry_variable(
        self, DisplayName, TelemetryName, NodeId, IoTCDataType
    ):
        mapTelemetryNodeVariable = {
            "DisplayName": DisplayName,
            "TelemetryName": TelemetryName,
            "NodeId": NodeId,
            "IoTCDataType": IoTCDataType,
        }
        return mapTelemetryNodeVariable

    # -------------------------------------------------------------------------------
    #   Function:   update_map_telemetry
    #   Usage:      Saves the generated Map Telemetry File
    # -------------------------------------------------------------------------------
    def update_map_telemetry(self):
        map_telemetry_file = MapTelemetry(self.logger)
        map_telemetry_file.update_file(self.map_telemetry)
        return
