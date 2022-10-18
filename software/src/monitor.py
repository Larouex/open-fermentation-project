# ==================================================================================
#   File:   monitor.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Main loop to monitor chamber, ambient and apply recipe lifcycle
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
from datetime import datetime, date
from sty import fg, bg, ef, rs
import RPi.GPIO as GPIO
import logging as Log

# AM 2315 - Chamber Temperature and Humidity
import board, busio, adafruit_am2320

# AM 2302 - Ambient Temperature and Humidity
import adafruit_dht

# our classes
from classes.config import Config
from classes.currentrecipe import CurrentRecipe
from classes.relay import Relay
from classes.recipephase import RecipePhase

# constants
import classes.constants as CONSTANT

# Set state moode
GPIO.setmode(GPIO.BCM)

# -------------------------------------------------------------------------------
#   Monitor Init
# -------------------------------------------------------------------------------
async def get_relay_pins(config):

    # get relay pins
    list = {
        "Humidifier": config["Relays"]["Pins"]["Humidifier"],
        "DeHumidifier": config["Relays"]["Pins"]["DeHumidifier"],
        "Heater": config["Relays"]["Pins"]["Heater"],
        "Chiller": config["Relays"]["Pins"]["Chiller"],
        "Fan": config["Relays"]["Pins"]["Fan"],
        "Light": config["Relays"]["Pins"]["Light"],
        "Open1": config["Relays"]["Pins"]["Open1"],
        "Open2": config["Relays"]["Pins"]["Open2"],
    }

    return list


# -------------------------------------------------------------------------------
#   Monitor Init
# -------------------------------------------------------------------------------
async def get_relays(logger, verbose, relay_pin_list):

    list = {
        "Humidifier": Relay(
            logger, verbose, relay_pin_list["Humidifier"], CONSTANT.OFF
        ),
        "DeHumidifier": Relay(
            logger, verbose, relay_pin_list["DeHumidifier"], CONSTANT.OFF
        ),
        "Heater": Relay(
            logger, verbose, relay_pin_list["Heater"], CONSTANT.OFF
        ),
        "Chiller": Relay(
            logger, verbose, relay_pin_list["Chiller"], CONSTANT.OFF
        ),
        "Fan": Relay(
            logger, verbose, relay_pin_list["Fan"], CONSTANT.ON
        ),
        "Light": Relay(
            logger, verbose, relay_pin_list["Light"], CONSTANT.OFF
        ),
        "Open1": Relay(
            logger, verbose, relay_pin_list["Open1"], CONSTANT.OFF
        ),
        "Open2": Relay(
            logger, verbose, relay_pin_list["Open2"], CONSTANT.OFF
        ),
    }

    return list


# -------------------------------------------------------------------------------
#   Monitor Recipe Sync on Start
# -------------------------------------------------------------------------------
async def init_recipe_sync(logger, verbose, config, current_recipe):

    try:

        # Get current checkpoint
        current_checkpoint = current_recipe["Current Checkpoint"]

        # Instantiate the recipe phase
        recipe_phase = RecipePhase(
            logger, verbose, current_recipe["Database"], current_recipe["Started"]
        )

        if verbose == True:
            print(bg.blue + "")
            print("-------------------------------------------------")
            print(" Monitor::Initialize Recipe and Checkpoint Sync")
            print("-------------------------------------------------" + bg.rs)
            print("Current Checkpoint->", current_checkpoint)

        # Let's check our data
        if current_checkpoint is None:

            print("ERROR Recipe Checkpoint IS NULL")

        else:

            # Recipe Information
            recipe_checkpoint = await recipe_phase.init_recipe_checkpoint()
            recipe_checkpoint_drift = await recipe_phase.delta_checkpoint(
                current_checkpoint
            )

            if verbose == True:
                print("Recipe Checkpoint->", recipe_checkpoint)
                print("Recipe Checkpoint Drift->", recipe_checkpoint_drift)

            if recipe_checkpoint_drift != 0:
                if verbose == True:
                    print(
                        "Correct Recipe Checkpoint Drift->",
                        config["Correct Recipe Checkpoint Drift"],
                    )

                if config["Correct Recipe Checkpoint Drift"] == True:
                    if verbose == True:
                        print("Correcting Recipe Checkpoint Drift...")
                        print(
                            " Setting Current Checkpoint->",
                            current_recipe["Current Checkpoint"],
                        )
                        print("  TO...")
                        print(" Recipe Checkpoint->", recipe_checkpoint)

                    update_current_recipe = CurrentRecipe(logger, verbose)
                    update_current_recipe_data = update_current_recipe.data
                    update_current_recipe_data["Current Checkpoint"] = recipe_checkpoint
                    update_current_recipe.update_file(update_current_recipe_data)

    except Exception as e:
        print("Exception::monitor.py(init_recipe_sync)->", e)
        return None

    return


# -------------------------------------------------------------------------------
#   Check Recipe for Checkpoint Advance (Moving through the Recipe Lifecycle)
# -------------------------------------------------------------------------------
async def check_recipe_progress(logger, verbose, current_recipe):

    try:

        # Instantiate the recipe phase
        recipe_phase = RecipePhase(
            logger, verbose, current_recipe["Database"], current_recipe["Started"]
        )

        # get the data
        recipe_phase_data = await recipe_phase.select_tracking_by_checkpoint(
            current_recipe["Current Checkpoint"]
        )

        loop_checkpoint = await recipe_phase.current_recipe_checkpoint()
        if loop_checkpoint != current_recipe["Current Checkpoint"]:

            await recipe_phase.complete_checkpoint(
                current_recipe["Current Checkpoint"], datetime.now()
            )

            if verbose == True:
                print("")
                print("-------------------------------------------------")
                print(" Monitor::Moving Checkpoint Forward")
                print("-------------------------------------------------")

            update_current_recipe = CurrentRecipe(logger, verbose)
            current_recipe["Current Checkpoint"] = loop_checkpoint
            update_current_recipe.update_file(current_recipe)

            await recipe_phase.started_checkpoint(
                current_recipe["Current Checkpoint"], datetime.now()
            )

            # Register [Advanced current checkpoint in recipe lifecycle] audit event
            audit_event = (
                "RECIPE",
                current_recipe["Current Checkpoint"],
                datetime.now(),
                "CHECKPOINT",
                "Advanced current checkpoint in recipe lifecycle.",
            )
            row = await recipe_phase.audit_event(audit_event)

        else:
            print("")

        if verbose == True:
            print("")
            print("-------------------------------------------------")
            print(" Monitor::Current Recipe")
            print("-------------------------------------------------")
            print("Started->", current_recipe["Started"])
            print("Checkpoint->", current_recipe["Current Checkpoint"])
            print("Recipe Phase Data->", recipe_phase_data)
            print("-------------------------------------------------")
            completed_recipe_percentage = float(
                recipe_phase_data["completeness"]
            ) * int(current_recipe["Current Checkpoint"])
            print("Percentage Complete: {:0.2f}%".format(completed_recipe_percentage))

    except Exception as e:
        print("Exception::monitor.py(check_recipe_progress)->", e)
        return None

    return


# -------------------------------------------------------------------------------
#   Humidity Cycle
# -------------------------------------------------------------------------------
async def humidity_cycle(logger, verbose, current_recipe, relay_list, humidity):

    try:
        # Instantiate the recipe phase
        recipe_phase = RecipePhase(
            logger, verbose, current_recipe["Database"], current_recipe["Started"]
        )

        # get the data
        recipe_phase_data = await recipe_phase.select_tracking_by_checkpoint(
            current_recipe["Current Checkpoint"]
        )

        if verbose == True:
            print("")
            print("-------------------------------------------------")
            print(" Monitor::Checking Humidity + Variance")
            print("-------------------------------------------------")

        # Do we do a DeHumidifier/Humidifier Cycle?
        if recipe_phase_data["humidity_desired"] > humidity:

            if verbose == True:
                print("Humidity LESS than Desired->", humidity)
                print("Humidity Desired->", recipe_phase_data["humidity_desired"])
                print("Humidity Variance->", recipe_phase_data["humidity_variance"])

            if (
                recipe_phase_data["humidity_desired"]
                + recipe_phase_data["humidity_variance"]
            ) > humidity:

                if verbose == True:
                    print("Humidity LESS than Desired + Variance->", humidity)
                    print(
                        "Humidity Desired + Variance->",
                        (
                            recipe_phase_data["humidity_desired"]
                            + recipe_phase_data["humidity_variance"]
                        ),
                    )

                # Register [Humidity Variance] audit event
                audit_event = (
                    recipe_phase_data["recipe_phase"],
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "HUMIDITY",
                    "Humidity LESS than Desired->{0}, Humidity Desired->{1}, Humidity Variance->{2}".format(
                        humidity,
                        recipe_phase_data["humidity_desired"],
                        recipe_phase_data["humidity_variance"],
                    ),
                )
                row = await recipe_phase.audit_event(audit_event)

                relay_list["Humidifier"].setRelayState(CONSTANT.ON)
                relay_list["DeHumidifier"].setRelayState(CONSTANT.OFF)
                print("Humidifier Relay is Engaged")

                # Register [Humidifier] audit event
                audit_event = (
                    recipe_phase_data["recipe_phase"],
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "HUMIDIFIER",
                    "Humidifier Relay is Engaged.",
                )
                row = await recipe_phase.audit_event(audit_event)

        elif recipe_phase_data["humidity_desired"] < humidity:

            if verbose == True:
                print("Humidity GREATER than Desired->", humidity)
                print("Humidity Desired->", recipe_phase_data["humidity_desired"])
                print("Humidity Variance->", recipe_phase_data["humidity_variance"])

            if (
                recipe_phase_data["humidity_desired"]
                - recipe_phase_data["humidity_variance"]
            ) < humidity:

                if verbose == True:
                    print("Humidity GREATER than Desired + Variance->", humidity)
                    print(
                        "Humidity Desired - Variance->",
                        (
                            recipe_phase_data["humidity_desired"]
                            - recipe_phase_data["humidity_variance"]
                        ),
                    )

                print("Humidity GREATER than Desired->", humidity)
                print("Humidity Desired->", recipe_phase_data["humidity_desired"])
                print("Humidity Variance->", recipe_phase_data["humidity_variance"])

                # Register [Humidity Variance] audit event
                audit_event = (
                    recipe_phase_data["recipe_phase"],
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "HUMIDITY",
                    "Humidity GREATER than Desired->{0}, Humidity Desired->{1}, Humidity Variance->{2}".format(
                        humidity,
                        recipe_phase_data["humidity_desired"],
                        recipe_phase_data["humidity_variance"],
                    ),
                )
                row = await recipe_phase.audit_event(audit_event)

                # Register [De-Humidity Variance] audit event
                audit_event = (
                    recipe_phase_data["recipe_phase"],
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "DEHUMIDIFIER",
                    "Humidity LESS than Desired->{0}, Humidity Desired->{1}, Humidity Variance->{2}".format(
                        humidity,
                        recipe_phase_data["humidity_desired"],
                        recipe_phase_data["humidity_variance"],
                    ),
                )
                row = await recipe_phase.audit_event(audit_event)

                relay_list["DeHumidifier"].setRelayState(CONSTANT.ON)
                relay_list["Humidifier"].setRelayState(CONSTANT.OFF)
                print("DeHumidifier Relay is Engaged")

                # Register [Humidifier] audit event
                audit_event = (
                    "RECIPE",
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "DEHUMIDIFIER",
                    "DeHumidifier Relay is Engaged.",
                )
                row = await recipe_phase.audit_event(audit_event)

    except Exception as e:
        print("Exception::monitor.py(humidity_cycle)->", e)
        return None

    return


# -------------------------------------------------------------------------------
#   Temperature Cycle
# -------------------------------------------------------------------------------
async def temperature_cycle(logger, verbose, current_recipe, relay_list, temperature):

    try:
        # Instantiate the recipe phase
        recipe_phase = RecipePhase(
            logger, verbose, current_recipe["Database"], current_recipe["Started"]
        )

        # get the data
        recipe_phase_data = await recipe_phase.select_tracking_by_checkpoint(
            current_recipe["Current Checkpoint"]
        )

        # Is the "Temperature Desired" GREATER THAN the "Current Temperature"?
        if recipe_phase_data["temperature_desired"] > temperature:

            if (
                recipe_phase_data["temperature_desired"]
                + recipe_phase_data["temperature_variance"]
            ) > temperature:

                # Register [Temperature Variance] audit event
                audit_event = (
                    recipe_phase_data["recipe_phase"],
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "TEMPERATURE",
                    "Temperature LESS THAN Desired Temperature->{0}, Temperature->{1}, Temperature Variance->{2}".format(
                        temperature,
                        recipe_phase_data["temperature_desired"],
                        recipe_phase_data["temperature_variance"],
                    ),
                )
                row = await recipe_phase.audit_event(audit_event)

                relay_list["Heater"].setRelayState(CONSTANT.ON)
                relay_list["Chiller"].setRelayState(CONSTANT.OFF)

                # Register [Heater] audit event
                audit_event = (
                    recipe_phase_data["recipe_phase"],
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "HEATER",
                    "Heater Relay is Engaged.",
                )
                row = await recipe_phase.audit_event(audit_event)

        # Is the "Temperature Desired" LESS THAN the "Current Temperature"?
        elif recipe_phase_data["temperature_desired"] < temperature:

            if (
                recipe_phase_data["temperature_desired"]
                - recipe_phase_data["temperature_variance"]
            ) < temperature:

                # Register [Temperature Variance] audit event
                audit_event = (
                    recipe_phase_data["recipe_phase"],
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "TEMPERATURE",
                    "Temperature GREATER THAN Desired Temperature->{0}, Temperature->{1}, Temperature Variance->{2}".format(
                        temperature,
                        recipe_phase_data["temperature_desired"],
                        recipe_phase_data["temperature_variance"],
                    ),
                )
                row = await recipe_phase.audit_event(audit_event)

                # Turn on the Chiller
                relay_list["Chiller"].setRelayState(CONSTANT.ON)
                relay_list["Heater"].setRelayState(CONSTANT.OFF)
                audit_event = (
                    recipe_phase_data["recipe_phase"],
                    current_recipe["Current Checkpoint"],
                    datetime.now(),
                    "CHILLER",
                    "Chiller Relay is Engaged.",
                )
                row = await recipe_phase.audit_event(audit_event)

    except Exception as e:
        print("Exception::monitor.py(humidity_cycle)->", e)
        return None

    return


# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

    # execution state from args
    verbose = False
    short_options = "hvd"
    long_options = ["help", "verbose", "debug"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))

    for current_argument, current_value in arguments:

        if current_argument in ("-h", "--help"):
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            print("HELP for test-verify-relays.py")
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            print("")
            print("  BASIC PARAMETERS...")
            print("")
            print("  -h or --help - Print out this Help Information")
            print(
                "  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging"
            )
            print(
                "  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging"
            )
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------"
            )
            return

        if current_argument in ("-v", "--verbose"):
            verbose = True
            Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.INFO)
            Log.info("Verbose Logging Mode...")
        else:
            Log.basicConfig(format="%(levelname)s: %(message)s")

        if current_argument in ("-d", "--debug"):
            Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
            Log.info("Debug Logging Mode...")
        else:
            Log.basicConfig(format="%(levelname)s: %(message)s")

        # Load the configuration file
        logger = Log
        config = Config(logger)
        config = config.data

        try:

            # init
            relay_pin_list = await get_relay_pins(config)
            relay_list = await get_relays(config, verbose, relay_pin_list)

            # set the fan on always
            # relay_list["Fan"].setRelayState(state_on)

            # Print Relay Configuration Values
            if verbose == True:
                print("")
                print("-------------------------------------------------")
                print(" Monitor::Assigned GPIO Pins for the Relays")
                print("-------------------------------------------------")
                for key in relay_pin_list:
                    print(key, ":", relay_pin_list[key])

            # Print Relay Configuration Values
            GPIO.setwarnings(False)
            if verbose == True:
                print("")
                print("-------------------------------------------------")
                print(" Monitor::Intial Relay GPIO State")
                print("-------------------------------------------------")
                for key in relay_list:
                    print(key, ":", relay_list[key].state)

            # Sleep time variables
            sleepTimeShort = 0.2
            sleepTimeLong = 1.5

            # init AM2315
            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = adafruit_am2320.AM2320(i2c)

            # init 2302 - setup pin to read
            pin = config["AmbientPin"]
            dhtDevice = adafruit_dht.DHT22(pin)

            # Load the current recipe file
            current_recipe = CurrentRecipe(logger, verbose)
            current_recipe = current_recipe.data
            await init_recipe_sync(logger, verbose, config, current_recipe)

            while True:

                try:

                    # Read the Chamber 2315 Sensor
                    chamber_temperature_c = sensor.temperature
                    chamber_temperature_f = chamber_temperature_c * (9 / 5) + 32
                    chamber_humidity = sensor.relative_humidity

                    if verbose == True:
                        print("")
                        print("-------------------------------------------------")
                        print(" Monitor::CHAMBER Temperature and Humidity")
                        print("-------------------------------------------------")
                        print("Temperature: {:0.2f}F".format(chamber_temperature_f))
                        print("Humidity: {:0.2f}%".format(chamber_humidity))

                except:
                    print("Read Error::monitor.py CHAMBER: AM2315")
                    continue

                try:

                    # Print the values to the serial port
                    ambient_temperature_c = dhtDevice.temperature
                    ambient_temperature_f = ambient_temperature_c * (9 / 5) + 32
                    humidity = dhtDevice.humidity

                    if verbose == True:
                        print("")
                        print("-------------------------------------------------")
                        print(" Monitor::AMBIENT Temperature and Humidity")
                        print("-------------------------------------------------")
                        print("Temperature: {:0.2f}F".format(ambient_temperature_f))
                        print("Humidity: {:0.2f}%".format(humidity))

                except:
                    print("Read Error::monitor.py AMBIENT: AM2302")
                    continue

                if verbose == True:
                    print("")
                    print("-------------------------------------------------")
                    print(" Monitor::Relay State")
                    print("-------------------------------------------------")
                    for key in relay_list:
                        print(key, ":", relay_list[key].state)
                        time.sleep(sleepTimeLong)

                await check_recipe_progress(logger, verbose, current_recipe)
                await humidity_cycle(
                    logger, verbose, current_recipe, relay_list, chamber_humidity
                )
                await temperature_cycle(
                    logger, verbose, current_recipe, relay_list, chamber_temperature_f
                )

        # End program cleanly with keyboard
        except KeyboardInterrupt:
            print("Exiting")

        # Reset GPIO settings
        GPIO.cleanup()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
