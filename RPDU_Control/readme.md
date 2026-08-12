# PowerSwitch App info
Tools to help with controlling the IP PowerSwitches.
[PowerSwitch_app.exe](./PowerSwitch_app.exe) is build from the [PowerSwitch_app.py](PowerSwitch_app.pyw) 
and can be run stand alone without Python.

## Prerequisite
* No prerequisite if running the .exe (Windows PC)
  *  (Optional) PowerSwitch details in .exe can be overwritten with the [PowerSwitchList.json](./PowerSwitchList.json) file
* [PowerSwitch_app.pyw](PowerSwitch_app.pyw)  tested with Python 3.7 and should have no further dependencies
  * See doc string within the script for more detail 
  
## Quick user guide
* Run the [PowerSwitch_app.exe](./PowerSwitch_app.exe) or [PowerSwitch_app.py](PowerSwitch_app.pyw) 
* Pick the right Scan-head from the drop down list
  * App should refresh with the current switch status
* Use the buttons to control the switch, ON/OFF etc.
* Since the machine names in the drop down are taken from the powerswitches itself, it is important to keep the details on the switches up to date!


## To build script as exe
* (if not already installed) pip install pyinstaller
* Perhaps best move PowerSwitch_app.py somewhere else to avoid cluttering the repo
  * run "pyinstaller PowerSwitch_app.spec" from cmd
    * grab exe from ./dist/
  * or run build.bat
  
  ## To add new RPDU units
* Log in to the RPDU. 
* Navigate to: About > Network 
* Add details to .json file
