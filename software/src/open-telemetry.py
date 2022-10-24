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

from classes.opentelemetry import OpenTelemetry

open_telemetry = OpenTelemetry()
logger = open_telemetry.export_log()
