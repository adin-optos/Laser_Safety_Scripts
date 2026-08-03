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

Button & TabItem


"""
#
# import subprocess
# import time
# from pywinauto import Application
#
#
# exe_path = r"C:\Program Files\Optos Inc\Optos Oban Capture\Optos.Oban.exe"
# working_dir = r"C:\Program Files\Optos Inc\Optos Oban Capture"
#
# exe_path = r"C:\Program Files\Optos Inc\Optos Oban Capture\FpgaDebugTool.exe"
# working_dir = r"C:\Program Files\Optos Inc\Optos Oban Capture"
#
# # Start OSTest with argument "1" (enables extended/debug features)
# subprocess.Popen([exe_path, "1"], cwd=working_dir)
# time.sleep(2)
#
# # Attach to the already running OSTest process using UI Automation (UIA)
# app = Application(backend="uia").connect(path=exe_path)
#
# # Get the main application window
# window = app.top_window()
#
#
# def open_tab(window, tab_title):
#     """
#     Opens a tab in OSTest using its visible title.
#
#     Args:
#         window: Main application window (pywinauto object)
#         tab_title: The visible name of the tab (string)
#     """
#     tab = window.child_window(title=tab_title, control_type="TabItem")
#     tab.select()
#     time.sleep(2)  # wait for UI to update
#
#
#
# open_tab(window, "Galvo")
#
#
# box = window.child_window(auto_id="step_size", control_type="Edit")
# box.set_edit_text("1")



"""
FPGA Debug tool automation

Purpose:
1. Launch FPGA Debug Tool with special mode ("1")
2. Connect to the running application
3. Navigate to a tab (e.g., "Galvo")
4. Interact with UI elements (e.g., edit box)

Usage:
    python -i Launch_CapApp.py
"""

from pathlib import Path
import subprocess
import time
import logging

from pywinauto import Application


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WAIT_TIME_SECONDS = 2

EXECUTABLE_PATH = Path(
    r"C:\Program Files\Optos Inc\Optos Oban Capture\FpgaDebugTool.exe"
)
WORKING_DIRECTORY = EXECUTABLE_PATH.parent


# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def launch_application(exe_path: Path, working_dir: Path) -> None:
    """
    Launch the target application.

    Args:
        exe_path: Path to executable
        working_dir: Working directory for process
    """
    logger.info(f"Launching application: {exe_path}")
    subprocess.Popen([str(exe_path), "1"], cwd=str(working_dir))
    time.sleep(WAIT_TIME_SECONDS)


def connect_to_application(exe_path: Path) -> Application:
    """
    Connect to a running instance of the application.

    Args:
        exe_path: Path to executable

    Returns:
        Connected pywinauto Application instance
    """
    logger.info("Connecting to running application...")
    return Application(backend="uia").connect(path=str(exe_path))


def debug_setup():
    """
    Debug entry point.

    Returns:
        Tuple of (app, window)
    """
    app = connect_to_application(EXECUTABLE_PATH)
    window = app.top_window()

    logger.info("Debug setup complete")

    return app, window


def open_tab(window, tab_title: str) -> None:
    """
    Open a tab in the application.

    Args:
        window: Main application window
        tab_title: Visible tab name
    """
    logger.info(f"Opening tab: {tab_title}")
    tab = window.child_window(title=tab_title, control_type="TabItem")
    tab.select()
    time.sleep(WAIT_TIME_SECONDS)


def set_edit_box_value(window, auto_id: str, value: str) -> None:
    """
    Set text in an edit box.

    Args:
        window: Main application window
        auto_id: Automation ID of the control
        value: Value to set
    """
    logger.info(f"Setting edit box ({auto_id}) to: {value}")
    edit_box = window.child_window(auto_id=auto_id, control_type="Edit")
    edit_box.set_edit_text(value)

def select_item(window, item_title: str) -> None:
    """
    Select an item from a list.

    Args:
        window: Main application window
        item_title: Visible title of the list item
    """
    logger.info(f"Selecting list item: {item_title}")
    item = window.child_window(title=item_title,control_type="ListItem",)
    item.select()

def click_button(window, button_title: str) -> None:
    """
    Click a button using its visible title.

    Args:
        window: Main application window
        button_title: Visible title of the button
    """
    logger.info(f"Clicking button: {button_title}")
    button = window.child_window(title=button_title, control_type="Button")
    button.click_input()  # more reliable than .click()



# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------
def main() -> None:
    """Main automation workflow."""
    try:
        # launch_application(EXECUTABLE_PATH, WORKING_DIRECTORY)

        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        open_tab(window, "Galvo")
        set_edit_box_value(window, "step_size", "1")
        set_edit_box_value(window, "capture_time", "10000")
        select_item(window, "1 H Sweep Start")
        select_item(window, "0 V ADC Pos H ADC Pos")

        click_button(window, "Arm capture")
        click_button(window, "Dump capture")
        click_button(window, "Dump LUTs")
        click_button(window, "Swap VH Drive LUTs")


        logger.info("Automation completed successfully.")

    except Exception as exc:
        logger.exception(f"Automation failed: {exc}")
        raise


def data_dumping() -> None:
    """Main automation workflow."""
    try:
        # launch_application(EXECUTABLE_PATH, WORKING_DIRECTORY)

        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        click_button(window, "Arm capture")
        click_button(window, "Dump capture")

        logger.info("Galvo data recorded.")

    except Exception as exc:
        logger.exception(f"Automation failed: {exc}")
        raise


def Galvo_LUT_Change() -> None:
    """Main automation workflow."""
    try:
        # launch_application(EXECUTABLE_PATH, WORKING_DIRECTORY)

        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        click_button(window, "Dump LUTs")
        click_button(window, "Swap VH Drive LUTs")

        logger.info("Automation completed successfully.")

    except Exception as exc:
        logger.exception(f"Automation failed: {exc}")
        raise


if __name__ == "__main__":
    main()


# uv run python dump_object_identifiers.py
# exit()
# python -i Launch_CapApp.py
# app, window = debug_setup()





"""debugging on scanhead:

python

import subprocess
import time
from pywinauto import Application
import sys

exe_path = r"C:\Program Files\Optos Inc\OSTest\OSTest.exe"
working_dir = r"C:\Program Files\Optos Inc\OSTest"

# Attach to the already running OSTest process using UI Automation (UIA)
app = Application(backend="uia").connect(path=exe_path)

# Get the main application window
window = app.top_window()


sys.stdout = open("ui_dump.txt", "w", encoding="utf-8")

window.print_control_identifiers()

"""


