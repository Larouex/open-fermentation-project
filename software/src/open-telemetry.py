# ==================================================================================
#   File:   open-telemetry.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Open Telemetry implementation
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import os, time
from typing import Iterable
import logging as Log

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import (
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    SERVICE_INSTANCE_ID,
    Resource,
)

from classes.otellogging import OtelLogging
from classes.otelspanenrichingprocessor import OtelSpanEnrichingProcessor
from classes.otelhistogram import OtelHistogram

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter

otel_logging = OtelLogging(Log, Log.NOTSET)
Log = otel_logging.get_export_log()
Log.error("open_telemetry testing with exception")
trace.set_tracer_provider(TracerProvider())

# trace.set_tracer_provider(
#    TracerProvider(
#        resource=Resource.create(
#            {
#                SERVICE_NAME: "open-telemetry",
#                SERVICE_NAMESPACE: "open-telemetry-namespace",
#                SERVICE_INSTANCE_ID: "open-telemetry-instance",
#            }
#        )
#    )
# )

span_enrich_processor = OtelSpanEnrichingProcessor(Log)
trace.get_tracer_provider().add_span_processor(span_enrich_processor)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("parent"):
    Log.warning("WARNING: Inside of span")
    Log.error("ERROR: Inside of span")

otel_histogram = OtelHistogram(Log)
otel_histogram.set_record(30.5, "RecipeProgress", 15)
otel_histogram.set_record(31.5, "RecipeProgress", 16)
