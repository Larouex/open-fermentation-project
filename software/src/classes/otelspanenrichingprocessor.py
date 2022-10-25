# ==================================================================================
#   File:   otelspanenrichingprocessor.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Creates the monitoring and instrumentation of the Saluminator and
#           sends the data to Azure Application Insights
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, sys, time, string, threading, asyncio, os, copy, socket
import logging

from opentelemetry.sdk.trace import SpanProcessor


class OtelSpanEnrichingProcessor(SpanProcessor):
    def __init__(self, Log):
        self._class = "OtelSpanEnrichingProcessor"
        self._method = "__init__"
        self._logger = Log

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(("10.254.254.254", 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

    # -------------------------------------------------------------------------------
    #   Function:   on_end
    #   Usage:      Add Attributes not Instrumented and Custom
    # -------------------------------------------------------------------------------
    def on_end(self, span):
        self._method = "on_end"

        try:

            span._name = "Updated-" + span.name
            IP = self.get_ip()
            print(IP)
            span._attributes["http.client_ip"] = IP
            span._attributes["http.client_city"] = "Normandy Park"
            span._attributes["saluminator_version"] = "V4.01"

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)
            return

        return
