# ==================================================================================
#   File:   recipephase.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Used to determine where in the Recipe Lifgecycle the current checkpoint
#           is located...
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import json, sys, time, string, threading, asyncio, os, copy
import logging
from datetime import datetime, date
import sqlite3
from sqlite3 import Error

from classes.config import Config
from classes.printtracing import PrintTracing

class RecipePhase:
    def __init__(self, Log, Verbose, Database, Started):
        
        self._logger = Log
        self._verbose = Verbose
        self._module = "RecipePhase"
        self._method = "__init__"

        # Load the configuration file
        self._config = Config(Log)

        # Tracing and Errors
        self._printtracing = PrintTracing(Log, Verbose, self._config)
        self._printtracing.printheader(self._module, self._method)

        # datetime calcs
        self.today = datetime.now()
        self._recipe_started = datetime.strptime(Started, "%Y-%m-%d %H:%M:%S.%f")
        self._hours_since_recipe_started = self.today - self._recipe_started
        self._hours_since_recipe_started = int(
            self._hours_since_recipe_started.total_seconds() / 3600
        )

        # __Verbose__
        if (self._verbose):
            _message = "Today: {today}".format(today = self.today)
            self._printtracing.print(_module, _method, _message, False)
            _message = "Recipe Started: {started}".format(started = self._recipe_started)
            self._printtracing.print(_module, _method, _message, True)
            _message = "Hours Elapsed Since Recipe Started: {elapsed}".format(elapsed = self._hours_since_recipe_started)
            self._printtracing.print(_module, _method, _message, True)

        # Create Database Connection
        self._database = Database
        self._connection = self.connect()

        return

    # -------------------------------------------------------------------------------
    #   Function:   connect
    #   Usage:      Connect to our pre configured recipe database
    # -------------------------------------------------------------------------------
    def connect(self):
        connection = None

        try:
            connection = sqlite3.connect(self._database)
            return connection
        except Error as ex:
            self._printtracing.forceprint(self._module, self._method, ex)

        return connection

    # -------------------------------------------------------------------------------
    #   Function:   view_tracking
    #   Usage:      Show all rows in tracking
    # -------------------------------------------------------------------------------
    def view_tracking(self):

        try:

            # Connect and Open tracking table
            cur = self._connection.cursor()

            # Select All Rows
            cur.execute("SELECT * FROM tracking")

            json_rows_result = []

            rows = cur.fetchall()
            for row in rows:
                json_result = {
                    "id": row[0],
                    "recipe_phase": row[1],
                    "recipe_hour": row[2],
                    "completeness": row[3],
                    "started_datetime": row[4],
                    "completed_datetime": row[5],
                    "temperature_format": row[6],
                    "temperature_desired": row[7],
                    "temperature_variance": row[8],
                    "temperature_run_time": row[9],
                    "temperature_idle_time": row[10],
                    "humidity_desired": row[11],
                    "humidity_variance": row[12],
                    "humidity_run_time": row[13],
                    "humidity_idle_time": row[14],
                }
                json_rows_result.append(json_result)

            return json_rows_result

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   view_tracking_start_end
    #   Usage:      Show first and last rows in tracking
    # -------------------------------------------------------------------------------
    def view_tracking_start_end(self):

        try:

            # Connect and Open tracking table
            cur = self._connection.cursor()

            json_rows_result = []

            # Select First row
            cur.execute("SELECT * FROM tracking WHERE id=(SELECT MIN(id) FROM tracking)")
            rows = cur.fetchall()
            for row in rows:
                json_result = {
                    "id": row[0],
                    "recipe_phase": row[1],
                    "recipe_hour": row[2],
                    "completeness": row[3],
                    "started_datetime": row[4],
                    "completed_datetime": row[5],
                    "temperature_format": row[6],
                    "temperature_desired": row[7],
                    "temperature_variance": row[8],
                    "temperature_run_time": row[9],
                    "temperature_idle_time": row[10],
                    "humidity_desired": row[11],
                    "humidity_variance": row[12],
                    "humidity_run_time": row[13],
                    "humidity_idle_time": row[14],
                }
                json_rows_result.append(json_result)

            # Select First row
            cur.execute("SELECT * FROM tracking WHERE id=(SELECT MAX(id) FROM tracking)")
            rows = cur.fetchall()
            for row in rows:
                json_result = {
                    "id": row[0],
                    "recipe_phase": row[1],
                    "recipe_hour": row[2],
                    "completeness": row[3],
                    "started_datetime": row[4],
                    "completed_datetime": row[5],
                    "temperature_format": row[6],
                    "temperature_desired": row[7],
                    "temperature_variance": row[8],
                    "temperature_run_time": row[9],
                    "temperature_idle_time": row[10],
                    "humidity_desired": row[11],
                    "humidity_variance": row[12],
                    "humidity_run_time": row[13],
                    "humidity_idle_time": row[14],
                }
                json_rows_result.append(json_result)

            return json_rows_result

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   select_tracking_by_checkpoint_json
    #   Usage:      Connect to our pre configured recipe database
    # -------------------------------------------------------------------------------
    async def select_tracking_by_checkpoint(self, checkpoint):

        try:

            # Connect and Open tracking table
            cur = self._connection.cursor()

            # Valid Checkpoint?
            cur.execute("SELECT * FROM tracking WHERE id=?", (checkpoint,))

            # get the checkpoint row
            row = cur.fetchone()
            json_result = {
                "id": row[0],
                "recipe_phase": row[1],
                "recipe_hour": row[2],
                "completeness": row[3],
                "started_datetime": row[4],
                "completed_datetime": row[5],
                "temperature_format": row[6],
                "temperature_desired": row[7],
                "temperature_variance": row[8],
                "temperature_run_time": row[9],
                "temperature_idle_time": row[10],
                "humidity_desired": row[11],
                "humidity_variance": row[12],
                "humidity_run_time": row[13],
                "humidity_idle_time": row[14],
            }
            return json_result

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   audit_event
    #   Usage:      Insert Audit event into the database
    # -------------------------------------------------------------------------------
    async def audit_event(self, task):

        try:

            sql = """ INSERT INTO audit(
                        recipe_phase,
                        recipe_hour,
                        event_datetime,
                        event_type,
                        event_description)
                    VALUES(?,?,?,?,?) """

            # Connect and Open Audit table
            cur = self._connection.cursor()
            cur.execute(sql, task)
            self._connection.commit()
            rowid = cur.lastrowid

            # __Verbose__
            if (self._verbose):
                _method = "audit_event"
                json_audit = verbose_audit_event(rowid)
                _message = "recipe_phase: {recipe_phase}".format(recipe_phase = json_audit["recipe_phase"])
                self._printtracing.print(_module, _method, _message, False)
                _message = "recipe_hour: {recipe_hour}".format(recipe_hour = json_audit["recipe_hour"])
                self._printtracing.print(_module, _method, _message, False)
                _message = "event_datetime: {event_datetime}".format(event_datetime = json_audit["event_datetime"])
                self._printtracing.print(_module, _method, _message, False)
                _message = "event_type: {event_type}".format(event_type = json_audit["event_type"])
                self._printtracing.print(_module, _method, _message, False)
                _message = "event_description: {event_description}".format(event_description = json_audit["event_description"])
                self._printtracing.print(_module, _method, _message, False)

            return rowid

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   verbose_audit_event
    #   Usage:      Print for Debug the Audit Event
    # -------------------------------------------------------------------------------
    async def verbose_audit_event(self, rowid):

        try:

            # Connect and Open audit table
            cur = self._connection.cursor()

            # Valid Audit Record?
            cur.execute("SELECT * FROM audit WHERE id=?", (rowid,))

            # get the checkpoint row
            row = cur.fetchone()
            json_result = {
                "id": row[0],
                "recipe_phase": row[1],
                "recipe_hour": row[2],
                "event_datetime": row[3],
                "event_type": row[4],
                "event_description": row[5],
            }
            return json_result

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   complete_checkpoint
    #   Usage:      Connect to recipe database and update completed checkpoint
    # -------------------------------------------------------------------------------
    async def complete_checkpoint(self, checkpoint, completed_datetime):

        try:

            # Connect and Open tracking table
            cur = self._connection.cursor()

            # Valid Checkpoint?
            cur.execute(
                "UPDATE tracking SET completed_datetime=? WHERE id=?",
                (completed_datetime, checkpoint),
            )
            self._connection.commit()

            return True

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   started_checkpoint
    #   Usage:      Connect to recipe database and update started checkpoint
    # -------------------------------------------------------------------------------
    async def started_checkpoint(self, checkpoint, started_datetime):

        try:

            # Connect and Open tracking table
            cur = self._connection.cursor()

            # Valid Checkpoint?
            cur.execute(
                "UPDATE tracking SET started_datetime=? WHERE id=?",
                (started_datetime, checkpoint),
            )
            self._connection.commit()

            return True

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   delta_checkpoint
    #   Usage:      How far adrift are we?
    # -------------------------------------------------------------------------------
    async def delta_checkpoint(self, checkpoint):

        try:

            if checkpoint != self._hours_since_recipe_started:
                return self._hours_since_recipe_started - checkpoint
            else:
                return 0

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   recipe_checkpoint
    #   Usage:      What does the Databse Say we should be at?
    # -------------------------------------------------------------------------------
    async def init_recipe_checkpoint(self):

        try:

            return self._hours_since_recipe_started

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   correct_checkpoint
    #   Usage:      Set current checkpoint to recipe checkpoint
    # -------------------------------------------------------------------------------
    async def correct_checkpoint(self):

        try:

            # Connect and Open tracking table
            cur = self._connection.cursor()

            # Valid Checkpoint?
            cur.execute(
                "UPDATE tracking SET started_datetime=? WHERE id=?",
                (datetime.now(), self.hours_since_started),
            )
            self._connection.commit()

            return True

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   current_recipe_checkpoint
    #   Usage:      Where are we now?
    # -------------------------------------------------------------------------------
    async def current_recipe_checkpoint(self):

        try:

            # datetime calcs
            today = datetime.now()
            hours_since_recipe_started = today - self._recipe_started
            hours_since_recipe_started = int(
                hours_since_recipe_started.total_seconds() / 3600
            )
            return hours_since_recipe_started

        except Exception as ex:
            self._printtracing.forceprint(self._module, self._method, ex)
            return None
