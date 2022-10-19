# ==================================================================================
#   File:   install.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Dynamic Installer for requirements specific to OS
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Gourmet Foods LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import sys, os, subprocess, platform

# debug
#print (hasattr(sys, 'real_prefix'))
#print (hasattr(sys, 'base_prefix'))
#print (sys.prefix)
#print (sys.base_prefix)

def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

if is_venv():
    os_name = platform.system()

    if (os_name == "Windows"):
        runcmd = 'python -m pip install -r requirements_windows.txt'
    elif (os_name == "Linus"):
        runcmd = 'python -m pip install -r requirements_raspbian.txt'

    cp = subprocess.run(runcmd)

    # process output with an API in the subprocess module:
    print("")
    print("INSTALLED....")
    print("")
    runcmd = 'python -m pip list'
    cp = subprocess.run(runcmd)

else:
    print("")
    print("------------------------------------------")
    print("WARNING")
    print('Do not run install.py outside of an activated Virtual Environment.')
    print('Please stop and read the ENVIONMENT.MD (for your Workstation) or ENVIONMENTRPI.MD for the Raspberry Pi on the Saluminator(R)')
    print("------------------------------------------")



