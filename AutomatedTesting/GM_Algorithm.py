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
from asyncio import sleep
from pathlib import Path
import subprocess
import time
import logging
import mss
import mss.tools
import os

from pywinauto import Application


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WAIT_TIME_SECONDS = 2

EXECUTABLE_PATH = Path(
    r"C:\Program Files\Optos Inc\OSTest\OSTest.exe"
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
    # logger.info("Connecting to running application...")
    return Application(backend="uia").connect(path=str(exe_path))


def debug_setup():
    """
    Debug entry point.

    Returns:
        Tuple of (app, window)
    """
    app = connect_to_application(EXECUTABLE_PATH)
    window = app.top_window()

    # logger.info("Debug setup complete")

    return app, window


def open_tab(window, tab_title: str) -> None:
    """
    Open a tab in the application.

    Args:
        window: Main application window
        tab_title: Visible tab name
    """
    # logger.info(f"Opening tab: {tab_title}")
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
    # logger.info(f"Setting edit box ({auto_id}) to: {value}")
    edit_box = window.child_window(auto_id=auto_id, control_type="Edit")
    edit_box.set_edit_text(value)

def select_item(window, item_title: str) -> None:
    """
    Select an item from a list.

    Args:
        window: Main application window
        item_title: Visible title of the list item
    """
    # logger.info(f"Selecting list item: {item_title}")
    item = window.child_window(title=item_title,control_type="ListItem",)
    item.select()


def click_button(window, button_title: str) -> None:
    """
    Click a button using its visible title.

    Args:
        window: Main application window
        button_title: Visible title of the button
    """
    # logger.info(f"Clicking button: {button_title}")
    button = window.child_window(title=button_title, control_type="Button")
    button.click_input()  # more reliable than .click()

def set_edit_box_value(window, auto_id: str, value: str):
    edit_box = window.child_window(auto_id=auto_id, control_type="Edit")
    edit_box.wait("ready visible enabled", timeout=5)

    edit_box.click_input()
    edit_box.type_keys("^a{BACKSPACE}")
    edit_box.type_keys(value)
    edit_box.type_keys("{ENTER}")  # some apps need this

def set_rev_time(window, value: str):
    # 1. Select the radio button
    radio = window.child_window(auto_id="RadioRevTime", control_type="RadioButton")
    radio.wait("ready", timeout=5)
    radio.select()   # ✅ use select for radio buttons

    # 2. Set the value
    edit = window.child_window(auto_id="TextBoxRevTime", control_type="Edit")
    edit.wait("ready", timeout=5)

    edit.click_input()
    edit.type_keys("^a{DEL}")
    edit.type_keys(value, pause=0.05)
    edit.type_keys("{ENTER}")

def set_sld_power(window, turn_on: bool):
    button = window.child_window(auto_id="SLDOnOffToggleButton", control_type="Button")
    button.wait("ready", timeout=5)

    state = button.window_text()

    if turn_on and state == "Off":
        button.click_input()

    elif not turn_on and state == "On":
        button.click_input()



def get_pm_values(window):
    texts = window.descendants(control_type="Text")

    pm1 = None
    pm2 = None

    get_pm1 = False
    get_pm2 = False

    for t in texts:
        txt = t.window_text().strip()

        # Detect labels
        if txt == "PM1:":
            get_pm1 = True
            continue

        if txt == "PM2:":
            get_pm2 = True
            continue

        # Capture values
        if get_pm1 and txt != "":
            pm1 = txt
            get_pm1 = False

        if get_pm2 and txt != "":
            pm2 = txt
            get_pm2 = False

        # Exit early if both found
        if pm1 is not None and pm2 is not None:
            break

    return pm1, pm2



# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------
def main() -> None:
    """Main automation workflow."""
    try:
        launch_application(EXECUTABLE_PATH, WORKING_DIRECTORY)

        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()
        click_button(window, "Restore")


        open_tab(window, "Hibiki Laser Power Calibration")
        window.child_window(auto_id="InitialiseSaEcs").click()
        time.sleep(2)
        # Get popup window
        dialog = app.top_window()
        # Click Yes
        dialog.child_window(title="Yes", control_type="Button").click()
        print("✅ ECS Initialised'")
        time.sleep(5)

        """Automated AGC Toggle"""
        time.sleep(2.5)
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

        print("✅ H AGC Toggle'")

        """GM Algo"""
        open_tab(window, "Hibiki Galvo HP DV")
        click_button(window, "PID Default")
        time.sleep(1)
        open_tab(window, "VGalvo")
        click_button(window, "PID Default")
        checkbox = window.child_window(auto_id="EnIlc", control_type="CheckBox")
        checkbox.click_input()
        logger.info("ECS Setup, ILC Enabled, Ready to set scan pattern.")

    except Exception as exc:
        logger.exception(f"Failed: {exc}")
        raise





def take_screenshot(galvo, freq, angle):
    # Create folder if it doesn't exist
    os.makedirs(galvo, exist_ok=True)

    filename = f"{galvo}/{freq}_{angle}.png"

    with mss.mss() as sct:
        mon = sct.monitors[0]  # full screen
        img = sct.grab(mon)
        mss.tools.to_png(img.rgb, img.size, output=filename)

    print(f"📸 Saved: {filename}")


# ✅ define inputs
freq = "125"
angle = "55"
galvo = "H_Galvo"
Scan = "H Scan"

def run_scan(freq, angle, galvo, Scan) -> None:
    try:
        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()


        # open_tab(window, "Hibiki Galvo HP DV")

        set_edit_box_value(window, "TextBoxFrameRate", freq)
        set_edit_box_value(window, "TextBoxAngleSweep", angle)

        set_rev_time(window, "1.1")

        click_button(window, "Set")

        click_button(window, Scan)
        time.sleep(0.7)

        set_sld_power(window, True)  # turn ON
        time.sleep(5.5)
        take_screenshot(galvo, freq, angle)
        time.sleep(2.5)
        pm1, pm2 = get_pm_values(window)
        print("H Galvo", freq, angle, "PM1:", pm1, "PM2:", pm2)
        with open("scan_log.txt", "a") as f: f.write(f"{freq}, {angle}, PM1: {pm1}, PM2: {pm2}\n")
        set_sld_power(window, False)  # turn OFF
        click_button(window, "Stop")


    except Exception as exc:
        logger.exception(f"Failed: {exc}")
        raise

    return pm1, pm2


if __name__ == "__main__":
    main()
    app, window = debug_setup()
    pm1, pm2 = run_scan(freq, angle)




#
# cd desktop
# python -i GM_Algorithm.py
# app, window = debug_setup()
#
# window = app.top_window()
# sys.stdout = open("ui_dump.txt", "w", encoding="utf-8")
# window.print_control_identifiers()

