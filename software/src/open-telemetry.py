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
import os
import logging

from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    LoggingHandler,
    set_log_emitter_provider,
)
from opentelemetry.sdk._logs.export import BatchLogProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

log_emitter_provider = LogEmitterProvider()
set_log_emitter_provider(log_emitter_provider)

exporter = AzureMonitorLogExporter(
    connection_string=os.environ[
        "InstrumentationKey=beec3397-2433-489c-833a-e4b9e4c4a1f6;IngestionEndpoint=https://westus2-2.in.applicationinsights.azure.com/;LiveEndpoint=https://westus2.livediagnostics.monitor.azure.com/"
    ]
)

log_emitter_provider.add_log_processor(BatchLogProcessor(exporter))
handler = LoggingHandler()

# Attach LoggingHandler to root logger
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)

logger.warning("Hello World!")
