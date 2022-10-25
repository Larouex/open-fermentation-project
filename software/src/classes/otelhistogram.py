# ==================================================================================
#   File:   otelhistogram.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Creates the monitoring and instrumentation of the Saluminator and
#           sends the data to Azure Application Insights
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, sys, time, string, threading, asyncio, os, copy
import logging

# our classes
from classes.config import Config
from classes.secrets import Secrets

from typing import Iterable
from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs.export import BatchLogProcessor

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider


# Experimental Logging Export
from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    LoggingHandler,
    set_log_emitter_provider,
)

from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter


class OtelHistogram:
    def __init__(self, Log, MeterName, DisplayName):
        self._class = "OtelHistogram"
        self._method = "__init__"

        try:

            self._logger = Log

            # load up configuration and secrets files
            self._config = Config(self._logger)
            self._secrets = Secrets(self._logger)

            # Create the Exporter
            self._metric_exporter = AzureMonitorMetricExporter(
                connection_string=self._secrets.ApplicationInsightsConnectionString
            )
            reader = PeriodicExportingMetricReader(self._metric_exporter)
            metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))
            meter = metrics.get_meter_provider().get_meter(MeterName)
            self._histogram = meter.create_histogram(MeterName, DisplayName)

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)

    # -------------------------------------------------------------------------------
    #   Function:   set_record
    #   Usage:      Record Values
    # -------------------------------------------------------------------------------
    def set_record(self, Value):
        self._method = "set_record"

        try:
            self._histogram.record(Value)

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)
            return

        return
