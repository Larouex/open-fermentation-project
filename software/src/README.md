[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<a href="https://www.open-fermentation-project.org/"><img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen"></a>&nbsp;<a href="https://apps.azureiotcentral.com/">
<img src="https://img.shields.io/badge/Azure IoT Central-Open%20Fermentation%20Project%20v1-blue"></a>&nbsp;<a href="https://www.saluminator.com/">
<img src="https://img.shields.io/badge/IoT-Saluminator%20Appliance%20v4-purple"></a>

<img src="../../assets/open-fermentation-project-logo-v2-750.png" width="250"/>

# Saluminator Appliance Software

## Contents

- [Saluminator Appliance Software](#saluminator-appliance-software)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Create Recipe Database](#create-recipe-database)
  - [Device Provisioning](#device-provisioning)

## Overview

The **Open Fermenation Project** has documented all of the code we use to connect, manage and monitor the Saluminator Appliance in a real world fermentation cycle. The code is all written Python and we take great care to fully document everthing. In the case where something needs clarity, is a bug or obtuse, make sure to create an issue in this repository so we can fix it for the community.

## Create Recipe Database

The Create Database script is the first script we run when we setup a new recipe for a fermentation cycle. The database technology we are using is based on SQLite and uses the Python sqllite package that is included in Python 3.x.

<a href="./CREATEDB.MD">Click here for details...</a>

## Device Provisioning

The Device Provisioning script is used to register and provision your device with Azure IoT Central.

<a href="./CREATEDB.MD">Click here for details...</a>
