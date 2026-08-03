"""
------------------------------------------------------------
OSTest Automation Script :
On system in cmd prompt
cd Desktop
python Dump_Oject_Identifiers.py

------------------------------------------------------------
Purpose:
1. Launch OSTest with special mode ("1")
2. Connect to the running application
3. Navigate to a tab, e.g., "Hibiki AGC Read Write" tab
4. Click buttons, e.g., "Read Initial H AGC" button
------------------------------------------------------------
"""

import subprocess
import time
from pywinauto import Application


exe_path = r"C:\Program Files\Optos Inc\Optos Oban Capture\Optos.Oban.exe"
working_dir = r"C:\Program Files\Optos Inc\Optos Oban Capture"

exe_path = r"C:\Program Files\Optos Inc\Optos Oban Capture\FpgaDebugTool.exe"
working_dir = r"C:\Program Files\Optos Inc\Optos Oban Capture"


# Path and Working directory to OSTest executable, #  (IMPORTANT for correct app startup)
exe_path = r"C:\Program Files\Optos Inc\OSTest\OSTest.exe"
working_dir = r"C:\Program Files\Optos Inc\OSTest"

# Start OSTest with argument "1" (enables extended/debug features)
subprocess.Popen([exe_path, "1"], cwd=working_dir)
time.sleep(1)

# Attach to the already running OSTest process using UI Automation (UIA)
app = Application(backend="uia").connect(path=exe_path)

# Get the main application window
window = app.top_window()


def open_tab(window, tab_title):
    """
    Opens a tab in OSTest using its visible title.

    Args:
        window: Main application window (pywinauto object)
        tab_title: The visible name of the tab (string)
    """
    tab = window.child_window(title=tab_title, control_type="TabItem")
    tab.select()
    time.sleep(2)  # wait for UI to update


# ------------------------------------------------------------

"""Automated AGC Toggle"""

open_tab(window, "Hibiki AGC Read Write")

buttons = [
    "bttnReadInitialHAgc",
    "bttnWriteHAgc",
    "bttnReadHAgc",
    "bttnWriteHInitial",
    "bttnReadHAgc",
]

for btn in buttons:
    window.child_window(auto_id=btn, control_type="Button").click()
    time.sleep(0.5)

print("✅ Successfully cycled H AGC'")

# ------------------------------------------------------------

open_tab(window, "Hibiki Laser Power Calibration")

# Click the button that triggers popup
window.child_window(auto_id="InitialiseSaEcs").click()

time.sleep(2)

# Get popup window
dialog = app.top_window()

# Click Yes
dialog.child_window(title="Yes", control_type="Button").click()


print("✅ ECS Initialised'")

time.sleep(5)

# "IrModeButton"

window.child_window(auto_id="SldModeButton").click()

time.sleep(5)

window.child_window(auto_id="CapNoneModeButton").click()



# ------------------------------------------------------------
"""ECS Trip Status"""

def check_for_trip(window):
    """
    Searches all text elements for the word 'tripped'
    """

    # Get all text controls in the window
    texts = window.descendants(control_type="Text")

    for t in texts:
        content = t.window_text()

        if "tripped" in content.lower():
            print(f"🚨 TRIP DETECTED: {content}")
            return True

    print("✅ No trip detected")
    return False

# open_tab(window, "Hibiki Laser Power Calibration")


time.sleep(1)
check_for_trip(window)

# ------------------------------------------------------------




"""debugging on scanhead:

python

exe_path = r"C:\Program Files\Optos Inc\OSTest\OSTest.exe"
working_dir = r"C:\Program Files\Optos Inc\OSTest"

# Attach to the already running OSTest process using UI Automation (UIA)
app = Application(backend="uia").connect(path=exe_path)

# Get the main application window
window = app.top_window()

import sys

sys.stdout = open("ui_dump.txt", "w", encoding="utf-8")

window.print_control_identifiers()

"""


