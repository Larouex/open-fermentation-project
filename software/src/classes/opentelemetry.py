# ==================================================================================
#   File:   opentelemetry.py
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

# Experimental Logging Export
from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    LoggingHandler,
    set_log_emitter_provider,
)

from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter


class OpenTelemetry:
    def __init__(self, Log, Level):

        self.logger = Log

        # load up configuration and mapping files
        self.config = []
        self.nodes = []
        self.load_config()

        # Load the secrets file
        self.secrets = []
        self.load_secrets()

        # Logging
        log_emitter_provider = LogEmitterProvider()
        set_log_emitter_provider(log_emitter_provider)

        # Create the Various Monitor Types
        log_exporter = AzureMonitorLogExporter(
            connection_string=self.secrets["ApplicationInsightsConnectionString"]
        )

        metric_exporter = AzureMonitorMetricExporter(
            connection_string=self.secrets["ApplicationInsightsConnectionString"]
        )

        trace_exporter = AzureMonitorTraceExporter(
            connection_string=self.secrets["ApplicationInsightsConnectionString"]
        )

        # Attach LoggingHandler to root logger
        log_emitter_provider.add_log_processor(BatchLogProcessor(log_exporter))
        handler = LoggingHandler()
        self.otel_logger.getLogger().addHandler(handler)
        self.otel_logger.getLogger().setLevel(Level)

    # -------------------------------------------------------------------------------
    #   Function:   export_log
    #   Usage:      Send a logging event to the Azure Monitor Exporter
    # -------------------------------------------------------------------------------
    async def export_log(self):

        try:

            logger = self.otel_logger.getLogger(__name__)
            logger.warning("Hello World!")

        except Exception as ex:
            self.logger.error("[ERROR] %s" % ex)
            self.logger.error("[TERMINATING] We encountered an error in Gateway")
            return

        return logger

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
        return

    # -------------------------------------------------------------------------------
    #   Function:   load_secrets
    #   Usage:      Loads the secrets
    # -------------------------------------------------------------------------------
    def load_secrets(self):

        # Load all the configuration
        secrets = Secrets(self.logger)
        self.secrets = secrets.data
        return
