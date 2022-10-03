# ==================================================================================
#   File:   opcserver.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Helper to translate how we think of Types in IoT Central to
#           the mapping of Variant Types as Defined in OPC/UA
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import logging


class VariantType:
    def __init__(self, Log):
        self.logger = Log

    def map_variant_type(self, iotc_data_type):

        data_types = {
            "boolean": 1,
            "date": 13,
            "dateTime": 13,
            "double": 11,
            "duration": 3,
            "float": 10,
            "geopoint": 3,
            "integer": 6,
            "long": 8,
            "string": 12,
            "time": 13,
        }
        return data_types.get(iotc_data_type, None)

        # OPCUA REFERENCE
        # Boolean = 1
        # Byte = 3
        # ByteString = 15
        # DataValue = 23
        # DateTime = 13
        # DiagnosticInfo = 25
        # Double = 11
        # ExpandedNodeId = 18
        # ExtensionObject = 22
        # Float = 10
        # Guid = 14
        # Int16 = 4
        # Int32 = 6
        # Int64 = 8
        # LocalizedText = 21
        # NodeId = 17
        # Null = 0
        # QualifiedName = 20
        # SByte = 2
        # StatusCode = 19
        # String = 12
        # UInt16 = 5
        # UInt32 = 7
        # UInt64 = 9
        # Variant = 24
        # XmlElement = 16
