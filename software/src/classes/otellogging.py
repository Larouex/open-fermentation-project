# ==================================================================================
#   File:   otellogging.py
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


class OtelLogging:
    def __init__(self, Log, Level):
        self._class = "OtelLogging"
        self._method = "__init__"

        try:

            self._logger = Log

            # load up configuration and secrets files
            self._config = Config(self._logger)
            self._secrets = Secrets(self._logger)

            # Logging
            log_emitter_provider = LogEmitterProvider()
            set_log_emitter_provider(log_emitter_provider)

            # Create the Various Monitor Types
            self._log_exporter = AzureMonitorLogExporter(
                connection_string=self._secrets.ApplicationInsightsConnectionString
            )

            self._metric_exporter = AzureMonitorMetricExporter(
                connection_string=self._secrets.ApplicationInsightsConnectionString
            )

            self._trace_exporter = AzureMonitorTraceExporter(
                connection_string=self._secrets.ApplicationInsightsConnectionString
            )

            # Attach LoggingHandler to root logger
            log_emitter_provider.add_log_processor(
                BatchLogProcessor(self._log_exporter)
            )
            handler = LoggingHandler()
            logging.getLogger().addHandler(handler)
            logging.getLogger().setLevel(Level)

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)

    # -------------------------------------------------------------------------------
    #   Function:   get_export_log
    #   Usage:      Return a OTel Logger
    # -------------------------------------------------------------------------------
    def get_export_log(self):
        self._method = "get_export_log"

        try:
            self._logger = logging.getLogger(__name__)

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)
            return

        return self._logger

    # -------------------------------------------------------------------------------
    #   Function:   trace_correlated_log_batch
    #   Usage:      Send a logging event to the Azure Monitor Exporter
    # -------------------------------------------------------------------------------
    def trace_correlated_log_batch(self):
        self._method = "trace_correlated_log_batch"

        try:

            with self._tracer.start_as_current_span("foo"):
                self._logger.warning("WARNING: Inside of span")

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)
            return

        return self._logger
