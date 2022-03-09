[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen">

<img src="./assets/open-fermentation-project-logo-v2_500px.png" width="500"/>

## Contents

- [Mission Statement](#mission-statement)
- [Welcome](#welcome)
  - [The Hardware (Overview)](#the-hardware)
  - [The Software (Overview)](#the-sofwtware)
  - [Recipe Phases](#recipe-phases)
    - [Incubation](#incubation)
    - [Curing](#curing)
    - [Finishing](#finishing)

## Mission Statement

Insert mission statement

## Welcome!

The Open Fermentation Project is...

- Reference Hardware for an Industrial IoT "Internet of Things" Fermentation Appliance
- The Automation Software to Manage a Fermentation Recipe Lifecycle
- Cloud Integration for Telemetry and Monitoring

## The Hardware

The curing appliance is branded and trademarked as the "Saluminator" and was developed by Larry W Jordan Jr for Larouex Gourmet Foods LLC. The trademark is registered for commercial projects.

We have opened up the design and how to build the device and you are encouraged to build one for yourself and the only restriction is that you do not pally the Saluminator our trademark for any commercial projects or usage.

We developed this appliance to bring precision curing and fermentation to home and custom curing chambers. The entire project is based on “open source” software and “open and available” components that anyone with basic engineering skills could put together our system. We share this all with you and you are welcome to just use the instructions here to build your system and/or we are happy to sell you everything you need from a complete DIY kit to everything fully assembled and ready to install.

We designed the Saluminator for the production of fermented products and specifically for the automation of dry curing meats and other recipes that require control over temperature, humidity and time. Connected to the power of the cloud and through the acquisition of stream telemetry and machine learning, the Saluminator IoT Automation tunes itself to variances in the ambient environment and the characteristics of your specific curing chamber

## The Software

Recipes in the Saluminator are fixed with a starting time and a ending time. The time between is the “Recipe Cycle” and it can be as simple as one set of settings applied to the whole fermentation cycle or more complex with three(3) phases in the cycle automatically managed by the Saluminator’s automation software.

### Recipe Phases

As an example, take a classic Tuscan salumi that consists of three distinct phases...

#### Incubation

This is the very first phase the salumi goes through in order to kick the starter culture and begin the fermentation. This consists of higher heat and humidity usually between 8 to 12 hours.

#### Curing

This is the longest time in the salumi and is marked by a consistent temperature and humidity with constant air flow. The goal is remove 30% of the water weight from the salumi.

#### Finishing

The final stage that typically keeps the temperature and humidity low to achieve minimal moisture and weight loss. This is an optional phase and is used to cure a bit longer and if you desire a harder texture.

### Managing Recipes

Managing recipes using the Saluminator’s automation system you can easily create a Recipe Cycle and save it for the future and easily apply it to a current run of a recipe. You can also create and save your recipes on the salumi.cloud and retrieve them from the machine. When you create a phase in the Recipe Cycle, you set the following…

### Recipe Parameters

Recipe management in the Saluminator is controlled through the setting of Parameters in the system and you set the following per phase…

#### Temperature

The consistent “desired” temperature you want for the curing chamber. You measure the temperature inside your chamber and monitor the ambient temperature outside the chamber.

#### Temperature Variance

This is the amount of temperature variance before the Heater or the Chiller kick in. For example, if the Desired Temperature is 70 Degrees Fahrenheit and the Temperature Variance is set to 3, then the chiller will kick in at 73 Degrees Fahrenheit and the heater at 67 Degrees Fahrenheit.

#### Temperature Run Time

This is a “per minute” setting that you can tell a device to run for a designated length of time. You can achieve fine control of the amount of change you get from the heater and chillers to run them for a set period of time and then monitor and perfect the amount of change to get the desired result in the cure chamber.

#### Temperature Idle Time

This is a “per minute” setting that you can set for the time to wait between runs for a heater or chiller.

#### Humidity

The desired RH for the phase of the recipe. It is common to “incubate” a recipe with higher heat and humidity to kick the starter. Then lower it for the cure cycle and then lower even more for the finish cycle.

#### Humidity Variance

This is the amount of temperature variance before the humidifier or the dehumidifier kick in. For example, If the desired Humidity is 65 RH and the Humidity Variance is 3, then the dehumidifier will kick in at 68 RH and the humidifier at 62 RH.

#### Humidity Run Time

This is a “per minute” setting that you can tell a device to run for a designated length of time. You can achieve fine control of the amount of change you get from the humidifier and dehumidifier to run them for a set period of time and then monitor and perfect the amount of change to get the desired value in the cure chamber.

#### Humidity Idle Time

This is a “per minute” setting that you can set for the time to wait between runs for a humidifier or dehumidifier.

#### Cycle Time Toggle

Toggle between Hours or Days used to measure time (24 or 1).

#### Cycle Time

Set the number of days or hours for this phase.

## The Cloud

Overview of the Metrics and Telemetry that Communicated to the Cloud for Analysis and Machine Learning.

### AZURE IOT CENTRAL

The Saluiminator has optional capabilities to connect and seamlessly integrate your appliance with Microsoft's Azure IoT Central subscription offering. Azure IoT Central provides scalable telemetry processing and visualizations, data export and connected communications with your Salmuninator. Learn More...

### TELEMETRY FEATURES

Each time the Samulinator takes a reading of a sensor, the data is sent to Azure IoT Central to record the values. This keeps an ongoing record of things like temperature and humidity readings.

#### State Changes

The Saluminator tracks the changes associated with the AC Relays that toggle the Humidifier, Dehumifier, Chiller and Heater. This data is aggregated along with the telemetry to support machine learning to create the perfect ambiance in the curing chamber.

#### Tracking Events

We track overrides, shut downs, restarts and other signficant events for the Saluminator.

### RECIPE REPORTING

#### Incubation Started

The date and time that the Incubate phase STARTED.

#### Incubation Ended

The date and time that the Incubate phase ENDED.

#### Incubation Percentage Completed

The amount of completion for the Incubate phase relative to the current date and time.

#### Cure Started

The date and time that the Cure phase STARTED. Cure Ended The date and time that the Cure phase ENDED.

#### Cure Percentage Completed

The amount of completion for the Cure phase relative to the current date and time.

#### Finish Started

The date and time that the Finish phase STARTED. Cure Ended The date and time that the Cure phase ENDED.

#### Finish Percentage Completed

The amount of completion for the Finish phase relative to the current date and time.

#### Checkpoint Hour

Checkpoint pointer to the exact hour that the Salumintor is at for the whole recipe cycle.

#### Last Reported from Device

The date and time that the last sending of the properties data from the Saluminator.
