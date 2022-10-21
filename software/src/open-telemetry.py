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
import getopt, sys, time, string, threading, asyncio, os
import logging as Log

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter.from_connection_string(
    "InstrumentationKey=beec3397-2433-489c-833a-e4b9e4c4a1f6;IngestionEndpoint=https://westus2-2.in.applicationinsights.azure.com/;LiveEndpoint=https://westus2.livediagnostics.monitor.azure.com/"
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

with tracer.start_as_current_span("hello"):
    print("Hello, World!")
