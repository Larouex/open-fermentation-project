[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<a href="https://www.open-fermentation-project.org/"><img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen"></a>&nbsp;<a href="https://apps.azureiotcentral.com/">
<img src="https://img.shields.io/badge/Azure IoT Central-Open%20Fermentation%20Project%20v1-blue"></a>&nbsp;<a href="https://www.saluminator.com/">
<img src="https://img.shields.io/badge/IoT-Saluminator%20Appliance%20v4-purple"></a>

<img src="../assets/open-fermentation-project-logo-v2-750.png" width="250"/>

# System Configuration Files

## <a name='Contents'></a>Contents

<!-- vscode-markdown-toc -->

- [Contents](#Contents)
- [Overview](#Overview)
- [Config](#Config)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

## <a name='Overview'></a>Overview

This document outlines all of the configuration options for the Saluminator&reg; device and scripts.

## <a name='Config'></a>Config

- **FILE**: <a href="./src/config.json">config.json</a>
- **LOCATION**: ./software/src/config.json

This is the core configuration file for the Saluminator&reg; System. Let's go through all of the details from the top of the file and work our way down...

```json
  "AppName": "SaluminatorV4",
  "Description": "Monitoring of Saluminator Fermentation System",
```

The **AppName** and **Description** are used as an overall way to identify the software in scripts and error messages. It can be any string value you want. For example, when you run scripts with the _--verbose_ or _--debug_ options, you will get a header and error messages with the app name and description.

```json
  "Enable Cloud Telemetry", true,
  "Telemetry Frequency In Seconds": 60,
  "Read Delay In Seconds": 5,
```

The **Enable Cloud Telemetry** option is true/false and indicates if the telemetery loop will send the data to Azure IoT Central.

The **Telemetry Frequency In Seconds** defines how frequently the telemetery loop is engaged to read the temperature and humidity (ambient and the chamber) and act on the data (engage the relays) and optionally to send the telemetry to the cloud based on the **Enable Cloud Telemetry** setting. This is an important setting as charges can be incurred when sending messages to the cloud and you want to be effecient and also generate enough data for proper visualizations.

The **Read Delay In Seconds** in used to place a pause after reading the ambient and chamber temperature and humidity sensors. This compensates in the telemetery loop for errors that the sensors may raise and adds the seconds to the overall loop time. The default is 5 and unless you are debugging, it is rarely needed.

```json
  "Temperature Format": "F",
```

The **Temperature Format** is used to indicate Fahrenheit (F) or Celsius (C) when monitoring the ambient and chamber temperature readings.

```json
  "NameSpace": "saluminatorIndustrialV4",
```

The **NameSpace** value is used to indicate the unique _namespace_ when communicating to IoT Central and in modeling for mapping to telemetry. This is covered more in depth in the [Azure IoT Central](./IOTCENTRAL.MD) document.

```json
  "Database Naming Pattern": "active_recipe_{recipe_name}.db",
```

The **Database Naming Pattern** is a string pattern that is used to insert the _recipe name_ into the file name to make it easy to understand the database from the file name. This value must exist in the recipes.json file and this relationship is explanined in the [Create Recipe Database](./IOTCENTRAL.MD) document.

```json
  "Correct Recipe Checkpoint Drift": true,
```

The **Correct Recipe Checkpoint Drift** is an important option that affects the way in which a recipe is _restarted_ after you monitoring has been interrupted for an active recipe. This could be because you stopped it manually or a power outage, etc.
