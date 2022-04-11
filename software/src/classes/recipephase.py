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


class RecipePhase:
    def __init__(self, Log, Verbose, Database, Started):
        
        self.logger = Log
        self._verbose = Verbose

        # datetime calcs
        self.today = datetime.now()
        self._recipe_started = datetime.strptime(Started, "%Y-%m-%d %H:%M:%S.%f")
        self._hours_since_recipe_started = self.today - self._recipe_started
        self._hours_since_recipe_started = int(
            self._hours_since_recipe_started.total_seconds() / 3600
        )

        if self._verbose == True:
            print("")
            print("-------------------------------------------------")
            print(" Class::RecipePhase (Lifecycle Data)")
            print("-------------------------------------------------")
            print("Today->", self.today)
            print("Recipe Started->", self._recipe_started)
            print(
                "Hours Elapsed Since Recipe Started-> ",
                self._hours_since_recipe_started,
            )

        # Create Database Connection
        self._database = Database
        self._connection = self.connect()

        if self._verbose == True:
            print("")
            print("-------------------------------------------------")
            print(" Class::RecipePhase (Database Access)")
            print("-------------------------------------------------")
            print("Database Location->", self._database)
            print("Connection->", self._connection)

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
        except Error as e:
            print("Exception::recipephase.py(connect)->", e)

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

        except Exception as e:
            print("Exception::recipephase.py(view_tracking)->", e)
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

        except Exception as e:
            print("Exception::recipephase.py(view_tracking)->", e)
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

        except Exception as e:
            print("Exception::recipephase.py(select_tracking_by_checkpoint)->", e)
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

            return cur.lastrowid

        except Exception as e:
            print("Exception::recipephase.py(audit_event)->", e)
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

        except Exception as e:
            print("Exception::recipephase.py(complete_checkpoint)->", e)
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

        except Exception as e:
            print("Exception::recipephase.py(started_checkpoint)->", e)
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

        except Exception as e:
            print("Exception::recipephase.py(delta_checkpoint)->", e)
            return None

    # -------------------------------------------------------------------------------
    #   Function:   recipe_checkpoint
    #   Usage:      What does the Databse Say we should be at?
    # -------------------------------------------------------------------------------
    async def init_recipe_checkpoint(self):

        try:

            return self._hours_since_recipe_started

        except Exception as e:
            print("Exception::recipephase.py(init_recipe_checkpoint)->", e)
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

        except Exception as e:
            print("Exception::recipephase.py(correct_checkpoint)->", e)
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

        except Exception as e:
            print("Exception::recipephase.py(current_recipe_checkpoint)->", e)
            return None
