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
    r"C:\Program Files\Optos Inc\Optos Oban Capture\Optos.Oban.exe"
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
    time.sleep(1)


def select_scan(window, app, scan_pattern: str) -> None:
    """
    Select a scan from the scan dropdown using a regex pattern.
    """
    logger.info(f"Selecting scan with pattern: {scan_pattern}")

    combo = window.child_window(
        auto_id="PopOutListScanSelection",
        control_type="ComboBox"
    )

    combo.click_input()
    time.sleep(1)

    # ✅ FIX: search inside combo, not top_window
    items = combo.descendants(control_type="ListItem")

    import re
    for item in items:
        text = item.window_text()
        logger.info(f"Checking: {text}")

        if re.search(scan_pattern, text):
            logger.info(f"Matched: {text}")
            item.click_input()
            time.sleep(13)
            return

    raise Exception(f"No scan matched pattern: {scan_pattern}")

def select_radio(window, radio_title: str) -> None:
    """
    Select a radio button using its visible title.

    Args:
        window: Main application window
        radio_title: Visible title of the radio button
    """
    logger.info(f"Selecting radio button: {radio_title}")

    rb = window.child_window(title=radio_title, control_type="RadioButton")
    rb.click_input()
    time.sleep(12)


# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------
def enter_patient_name() -> None:
    """Main automation workflow."""
    try:
        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        # Enter patient name
        field = window.child_window(control_type="Edit")
        field.click_input()
        field.type_keys("test", with_spaces=True)

        item = window.child_window(title="test test", control_type="Text")
        item.click_input()

        time.sleep(1)
        click_button(window, "To capture")
        click_button(window, "Table height OK")

        time.sleep(13)
        select_radio(window, "Left eye")

        # click_button(window, "Start OCT setup")
        # time.sleep(14)

    except Exception as exc:
        logger.exception(f"Automation failed: {exc}")
        raise

def main(scan_pattern) -> None:
    """Main automation workflow."""
    try:
        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        # ✅ Use input pattern here
        select_scan(window, app, scan_pattern)

    except Exception as exc:
        logger.exception(f"Automation failed: {exc}")
        raise


def click_return_arrow(window):
    window.child_window(
        auto_id="HeaderSite", control_type="Button").click_input()


def finish_patient() -> None:
    """Main automation workflow."""
    try:
        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        click_return_arrow(window)
        time.sleep(4)
        click_button(window, "Finished patient")
        time.sleep(6)

    except Exception as exc:
        logger.exception(f"failed: {exc}")
        raise




scan_patterns = [
    "RetinaScanDefinition",
    "MultiLineScanDefinition",
    "MultiLineCrossScanDefinition",
    "AsOctChamberScanDefinition",
    "AsOctEpitheliumScanDefinition",
    "AsOctLineScanDefinition",
    "OctAMaculaScanDefinition",
    "OctaONHScanDefinition",
    "PosteriorWideOctScanDefinition"
]

if __name__ == "__main__":
    main(scan_patterns[2])

    # uv run python dump_object_identifiers.py
    # exit()
    # python -i Launch_CapApp.py
    # app, window = debug_setup()

    # python -i Launch_App1.py
    # app, window = debug_setup()
    #
    # window = app.top_window()
    # sys.stdout = open("ui_dump.txt", "w", encoding="utf-8")
    # window.print_control_identifiers()