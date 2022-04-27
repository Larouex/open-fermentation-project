[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<a href="https://www.open-fermentation-project.org/"><img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen"></a>&nbsp;<a href="https://apps.azureiotcentral.com/">
<img src="https://img.shields.io/badge/Azure IoT Central-Open%20Fermentation%20Project%20v1-blue"></a>&nbsp;<a href="https://www.saluminator.com/">
<img src="https://img.shields.io/badge/IoT-Saluminator%20Appliance%20v4-purple"></a>

# The Hardware A/C Path

<img src="../assets/open-fermentation-project-logo-v2-750.png" width="250"/>

## Overview

Let's walk through the configuration of the A/C path of electricity for the Saluminator&reg; System...

* A/C comes in via the Main Switch
* Live wire is passed through the A/C Wattage and Voltage Monitoring Component
* Live Wire is Connected to the P2 connection on the A/C Distribution and Fuse Board
* Live Wires (8) are Connected to the 8 Way Relay Board (Common)
* Live Wires (6) are Connected to the Normally Open Output of the Relay Board to the Live Connection for each A/C Plug
* Neutral Wire is Connected from the Main Switch to the P1 connection on the A/C Distribution and Fuse Board
* Neutral Wires(6) are Connected via the  for each A/C Plug
* Each A/C Plug Ground is Connected to Common Ground

<img src="../assets/ac-path.png"/>

Here is a view of just this part of the assembly of the hardware...

<img src="../assets/ac-view-hw.png"/>

