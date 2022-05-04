[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<a href="https://www.open-fermentation-project.org/"><img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen"></a>&nbsp;<a href="https://apps.azureiotcentral.com/">
<img src="https://img.shields.io/badge/Azure IoT Central-Open%20Fermentation%20Project%20v1-blue"></a>&nbsp;<a href="https://www.saluminator.com/">
<img src="https://img.shields.io/badge/IoT-Saluminator%20Appliance%20v4-purple"></a>

# The Hardware D/C Path

<img src="../assets/open-fermentation-project-logo-v2-750.png" width="250"/>

## Overview

Let's walk through the configuration of the A/C path of electricity for the Saluminator&reg; System...

- A/C comes in via the Main Switch
- Live wire is passed through the A/C Wattage and Voltage Monitoring Component
- Live Wire is Connected to the P2 connection on the A/C Distribution and Fuse Board
- Live Wire from P2 is Connected to the DC Power Block Live Wire Connection
- Nuetral Wire from P1 is Connected to the DC Power Block Nuetral Wire Connection
- DC Power Block Ground is Connected to Common Ground
- Live VCC 5V DC is connected to Passive Distribution Block
- Ground GND 5V DC is connected to Passive Distribution Block

<img src="../assets/dc-path.png"/>
