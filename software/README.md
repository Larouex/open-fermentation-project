[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<a href="https://www.open-fermentation-project.org/"><img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen"></a>&nbsp;<a href="https://apps.azureiotcentral.com/">
<img src="https://img.shields.io/badge/Azure IoT Central-Open%20Fermentation%20Project%20v1-blue"></a>&nbsp;<a href="https://www.saluminator.com/">
<img src="https://img.shields.io/badge/IoT-Saluminator%20Appliance%20v4-purple"></a>

<img src="../assets/open-fermentation-project-logo-v2-750.png" width="250"/>

# The Software

The software for the **Saluminator&reg;** and the **Open Fermentation Project SPC** is located in this section of the repository. The **Quick Start** document is located here and it outlines the sequence of installation of the tool chain and how to setup the Raspberry Pi to automation the fermentation process, get connected to Azure Iot Central and monitor the lifecycle of a fermentation recipe.

The content below is the deep dive into each of the Python scripts, modules, classes and cloud integration for Azure Iot Central to create your own implementation end to end.

## Contents

- [Overview](#overview)

## Recipe Management

- [Recipe Management Details](./RECIPES.MD)
  Recipes in the Saluminator&reg; are fixed with a starting time and a ending time.

## Saluminator&reg; Software

The following docs are deep-dives into the specific scripts and modules that comprise the Saluminator&reg; system. I recommmend that you read them in the order intended to get an overview of the usage and sequence when initially setting up your system and then monitoring the recipe.

- [Configure System Files](./CONFIGURE.MD)
  Guidance and suggestions for the json files for configuration, security, recipes, etc.

- [Create Database](./CREATEDB.MD)
  The Create Database script is the first script we run when we setup a new recipe for a fermentation cycle.

- [Provision Device to Azure IoT Central](./PROVISION.MD)
  The Create Database script is the first script we run when we setup a new recipe for a fermentation cycle.
