"""
------------------------------------------------------------
Dump all tabs & buttons indentifiers: dir ui_dump.txt
Button names can be found in the .XMAL code of the relevant tab
https://github.com/Optos-plc/oban-capture/tree/develop/Source/Optos/Tools/OSTest/OSTest/Views
------------------------------------------------------------
"""


import subprocess
import time
import sys
from pywinauto import Application

exe_path = r"C:\Program Files\Optos Inc\OSTest\OSTest.exe"
working_dir = r"C:\Program Files\Optos Inc\OSTest"

# Redirect output to file
sys.stdout = open("ui_dump.txt", "w", encoding="utf-8")

subprocess.Popen([exe_path, "1"], cwd=working_dir)

time.sleep(5)

app = Application(backend="uia").connect(path=exe_path)
window = app.top_window()

# This now writes to file instead of CMD
window.print_control_identifiers()




import sys

sys.stdout = open("ui_dump.txt", "w", encoding="utf-8")

window.print_control_identifiers()

# C:\Users\ServiceAdmin
