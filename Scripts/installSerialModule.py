''' This script allows you to install the pyserial module on you Maya Python interpreter
    Execute this on a Script Editor inside Maya and restart the software
'''

import subprocess

# IMPORTANT: Change the path to your Maya Version
mayapyPath = r"C:\Program Files\Autodesk\Maya<version>\bin\mayapy.exe"

command = [mayapyPath, "-m", "pip", "install", "pyserial"]

subprocess.run(command, shell = True)
