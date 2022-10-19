[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<a href="https://www.open-fermentation-project.org/"><img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen"></a>&nbsp;<a href="https://apps.azureiotcentral.com/">
<img src="https://img.shields.io/badge/Azure IoT Central-Open%20Fermentation%20Project%20v1-blue"></a>&nbsp;<a href="https://www.saluminator.com/">
<img src="https://img.shields.io/badge/IoT-Saluminator%20Appliance%20v4-purple"></a>

<img src="../assets/open-fermentation-project-logo-v2-750.png" width="250"/>

# Setting up the Environment

## Contents

- [Setting up the Environment](#setting-up-the-environment)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Setting up the Development Toolchain for your Workstation](#setting-up-the-development-toolchain-for-your-workstation)
    - [Install Git](#install-git)
      - [Install/Update on Windows](#installupdate-on-windows)
      - [Install/Update on Mac](#installupdate-on-mac)
      - [Install/Update on Linux/Raspbian](#installupdate-on-linuxraspbian)
    - [Install Visual Studio Code](#install-visual-studio-code)
    - [Install Python](#install-python)
    - [Upgrading Pip](#upgrading-pip)
    - [Install all the Tools for Visual Studio Code](#install-all-the-tools-for-visual-studio-code)
  - [Get the Code!](#get-the-code)
    - [Powershell](#powershell)
    - [Linux/Mac BASH INSTRUCTIONS](#linuxmac-bash-instructions)
    - [Install the Requirements for the Virtual Environment and Python](#install-the-requirements-for-the-virtual-environment-and-python)
      - [Powershell](#powershell-1)
      - [Linux/Mac BASH INSTRUCTIONS](#linuxmac-bash-instructions-1)
    - [Congratulations! Your Development "Workstation" is configured. Next, let's setup the environment on the Raspberry Pi.](#congratulations-your-development-workstation-is-configured-next-lets-setup-the-environment-on-the-raspberry-pi)

## Overview

This document walks you through the setup of your development environment on your main machine (desktop or laptop) and the Raspbian OS (Debian) operating system environment on the Raspberry Pi for the Saluminator&reg;. Setup on your workstation involves configuring the development toolchain (everything that is needed to edit/iterate/build/deploy the software) and on the Raspberry Pi, the latest versions and the virtual environment for isolation of the Saluminator&reg; software when you are testing and running the applications.

**NOTE:** This is not a comprehensive and there are a number of issues you may encounter with versioning and other little nits. That is what the interwebs are for :)

## Setting up the Development Toolchain for your Workstation

I used the generic term "Workstation" as a way to differentiate that this is the main computer (workstation, laptop, etc.) that you use to do your primary development work. We assume it exists on the same network (if using an ethernet connection) and you can install the tools that will allow you to connect and develop code remotely on the Raspberry Pi.

### Install Git

Git is the tool we use for version control and management of software assets. Our workshop will use it to clone the modules and also to merege and contribute to the respository.

Validate that Git is installed and check the version...
```
git --version
```
#### Install/Update on Windows
Open a Powershell window...
```
git update-git-for-windows
```

#### Install/Update on Mac
Open a terminal window and install Homebrew...
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Install/Update Git
```bash
brew upgrade git
```

#### Install/Update on Linux/Raspbian
Open a Terminal window...
```
sudo apt update
sudo apt upgrade
```

[LINK: Git Installation Page](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Install Visual Studio Code

This is the IDE we will use to write code, deploy to the RPi, etc.

[LINK: Visual Studio Code Installation Page](https://code.visualstudio.com/download)

### Install Python

Pyhon is the language we will use to build applications for the Raspberry Pi

From the Python Org:

- Python is powerful... and fast;
- plays well with others;
- runs everywhere;
- is friendly & easy to learn;
- is Open.

[LINK: Python 3 Installation Page](https://www.python.org/downloads/)

### Upgrading Pip

Pip is the package manager we will use to download packages

On Linux or macOS (Open Terminal):

```
pip install -U pip
```

On Windows (from a CMD window or Powershell):

```bash
python -m pip install -U pip
```

### Install all the Tools for Visual Studio Code

These are a set of tools we will use to develop our apps on the Raspberry Pi. You can open the Extensions sidebar with "Shift+Ctrl+X) or click the icon in the side navigator bar.

![alt text](../assets/vs-code-python-sml.png "VS Code Python")

![alt text](../assets/vs-code-remote-ssh-sml.png "VS Code Remote SSH")

![alt text](../assets/vs-code-remote-edit-sml.png "VS Code Remote SSH Edit")

## Get the Code!

The next step is to bring this repository to your development machine so you can work with all of the code and scripts. If you want to contribute, you can also create and submit Oull Requests!

### Powershell
Open up a Powershell window and type in the following...

```ps1
cd \
mkdir Projects
cd Projects
git clone https://github.com/Larouex/open-fermentation-project.git
cd open-fermentation-project
dir
```
You should see something similar to the following output...
```ps1

    Directory: C:\Projects\open-fermentation-project

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          4/4/2022  10:52 AM                assets
d-----         3/29/2022   8:57 AM                cloud
d-----         3/29/2022   8:57 AM                hardware
d-----         4/11/2022  10:48 AM                software
-a----         3/14/2022   8:47 AM           6148 .DS_Store
-a----         4/11/2022  11:49 AM             52 .gitignore
-a----         3/14/2022   2:48 PM          35497 LICENSE.md
-a----         3/29/2022   8:57 AM           6611 README.md
```

### Linux/Mac BASH INSTRUCTIONS
Open up a Terminal window and type in the following...

```bash
cd \
mkdir Projects
cd Projects
git clone https://github.com/Larouex/open-fermentation-project.git
cd open-fermentation-project
ls -l
```
You should see something similar to the following output...
```bash
total 84
drwxr-xr-x 1 larryj 1049089     0 Oct  3 13:47 assets/
drwxr-xr-x 1 larryj 1049089     0 Oct  3 13:45 assets-editing/
drwxr-xr-x 1 larryj 1049089     0 Mar 29  2022 cloud/
drwxr-xr-x 1 larryj 1049089     0 May 26 12:52 hardware/
-rw-r--r-- 1 larryj 1049089 35497 Mar 14  2022 LICENSE.md
-rw-r--r-- 1 larryj 1049089  6573 Oct  3 13:45 README.md
drwxr-xr-x 1 larryj 1049089     0 Oct 18 09:34 software/
```

### Install the Requirements for the Virtual Environment and Python
This next set of steps are all executed from the command line and will result in a virtual environment that supports the running of the Saluminator&reg; scripts and modifications, etc.

#### Powershell
First, open a powershell terminal in Visual Studio Code and set the powershell execution policy to allow scripts...
```ps1
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```
Next, let's make sure we are in the right folder structure...
```ps1
cd \
cd .\Projects\open-fermentation-project\software\
```
Next, install the Python Virtual Environment...
```ps1
python -m pip install --user virtualenv
```
Create the virtual environment for the Saluminator&reg; software..
```ps1
python -m venv ./.saluminatorv4-venv/dev
```
Start (Activate) the virtual environment..
```ps1
.\.saluminatorv4-venv\dev\Scripts\Activate.ps1
```
Install the requirements...
```ps1
python install.py
```
Verify the Environment...
```ps1
cd src
python test-verify-env-dev.py
```
You will see something similar to the output below...
```ps1
-------------------------------------------------------------
APP NAME: SaluminatorV4
APP DESC: Monitoring of Saluminator Fermentation System
SCRIPT: test-verify-env-dev.py
METHOD: main()
-------------------------------------------------------------
Testing and Verifying the Environment...
(Config) SUCCESS: Loaded the Configuration File (config.json)
(DeviceCache) SUCCESS: Loaded the Device Cache File (devicecache.json)
(Secrets) SUCCESS: Loaded the Secrets File (secrets.json)
(Recipes) SUCCESS: Loaded the Recipes File (recipes.json)
```
**NOTE:** You can examine the contents of the various json files by adding the --verbose option to the test-verify-env-dev.py script.

#### Linux/Mac BASH INSTRUCTIONS
Open a bash terminal in Visual Studio Code and install the Python Virtual Environment support...
```bash
python -m pip install --user virtualenv
```
Next, let's make sure we are in the right folder structure...
```bash
cd /
cd ./Projects/open-fermentation-project/software/
```
Create the virtual environment for the Saluminator&reg; software..
```bash
python -m venv ./.saluminatorv4-venv/dev
```
and then start the virtual environment..

```bash
source ./.saluminatorv4-venv/dev/Scripts/activate
```
Install the requirements...
```bash
python install.py
```
Verify the Environment...
```bash
cd src
python test-verify-env-dev.py
```
You will see something similar to the output below...
```bash
-------------------------------------------------------------
APP NAME: SaluminatorV4
APP DESC: Monitoring of Saluminator Fermentation System
SCRIPT: test-verify-env-dev.py
METHOD: main()
-------------------------------------------------------------
Testing and Verifying the Environment...
(Config) SUCCESS: Loaded the Configuration File (config.json)
(DeviceCache) SUCCESS: Loaded the Device Cache File (devicecache.json)
(Secrets) SUCCESS: Loaded the Secrets File (secrets.json)
(Recipes) SUCCESS: Loaded the Recipes File (recipes.json)
```
**NOTE:** You can examine the contents of the various json files by adding the --verbose option to the test-verify-env-dev.py script.

### Congratulations! Your Development "Workstation" is configured. Next, let's setup the environment on the Raspberry Pi.
