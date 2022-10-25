# ==================================================================================
#   File:   otelmetering.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Creates the monitoring and instrumentation of the Saluminator and
#           sends the data to Azure Application Insights
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import os
from typing import Iterable

# our classes
from classes.config import Config
from classes.secrets import Secrets

from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter

class OtelMetering:
    def __init__(self, Log):
        self._class = "OtelMetering"
        self._method = "__init__"

        try:

            self._logger = Log

            # load up configuration and secrets files
            self._config = Config(self._logger)
            self._secrets = Secrets(self._logger)

            # Create the Various Monitor Types
            self._metric_exporter = AzureMonitorMetricExporter(
                connection_string=self._secrets.ApplicationInsightsConnectionString
            )

            self._reader = PeriodicExportingMetricReader(self._metric_exporter, export_interval_millis=5000)
            metrics.set_meter_provider(MeterProvider(metric_readers=[self._reader]))

            # Create a namespaced meter
            self._meter = metrics.get_meter_provider().get_meter("Chamber")

        except Exception as ex:
            self._logger.error("%s:%s->%s", self._class, self._method, ex)



    # Callback functions for observable instruments
    def observable_counter_func(self, options: CallbackOptions) -> Iterable[Observation]:
        yield Observation(1, {})


    def observable_up_down_counter_func(
        self,
        options: CallbackOptions,
    ) -> Iterable[Observation]:
        yield Observation(-10, {})


    def observable_gauge_func(self, options: CallbackOptions) -> Iterable[Observation]:
        yield Observation(9, {})

    def instrument(self):

        # Counter
        counter = self._meter.create_counter("progress")
        counter.add(1)

        # Async Counter
        observable_counter = self._meter.create_observable_counter(
            "observable_counter", [self.observable_counter_func]
        )

        # UpDownCounter
        updown_counter = self._meter.create_up_down_counter("updown_counter")
        updown_counter.add(1)
        updown_counter.add(-5)

        # Async UpDownCounter
        observable_updown_counter = self._meter.create_observable_up_down_counter(
            "observable_updown_counter", [self.observable_up_down_counter_func]
        )

        # Histogram
        histogram = self._meter.create_histogram("histogram")
        histogram.record(99.9)

        # Async Gauge
        gauge = self._meter.create_observable_gauge("gauge", [self.observable_gauge_func])
