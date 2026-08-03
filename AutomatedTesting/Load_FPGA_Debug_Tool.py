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
        launch_application(EXECUTABLE_PATH, WORKING_DIRECTORY)

        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        open_tab(window, "Galvo")
        set_edit_box_value(window, "step_size", "1")
        set_edit_box_value(window, "capture_time", "40000")
        select_item(window, "1 H Sweep Start")
        select_item(window, "0 V ADC Pos H ADC Pos")

        logger.info("FPGA Debug Tool Luanched & Configured.")

    except Exception as exc:
        logger.exception(f"FPGA Debug Tool failed: {exc}")
        raise

if __name__ == "__main__":
    main()


def data_dumping() -> None:
    """Main automation workflow."""
    try:
        # launch_application(EXECUTABLE_PATH, WORKING_DIRECTORY)

        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()
        click_button(window, "Arm capture")
        time.sleep(6)
        click_button(window, "Dump capture")


        logger.info("Galvo data recorded.")

    except Exception as exc:
        logger.exception(f"Dumping failed: {exc}")
        raise

def LUT_dumping() -> None:
    """Main automation workflow."""
    try:
        # launch_application(EXECUTABLE_PATH, WORKING_DIRECTORY)

        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()
        click_button(window, "Dump LUTs")

        logger.info("LUT data recorded.")

    except Exception as exc:
        logger.exception(f"Dumping failed: {exc}")
        raise


def Galvo_LUT_Change(file_name) -> None:
    """Update Galvo LUT using provided file name."""
    try:
        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        # ✅ Correct path handling
        directory = r"C:\Optos Data\oct_raw_data"
        full_path = f"{directory}\\{file_name}"

        # ✅ Correct edit box (from your UI dump)
        set_edit_box_value(window,"write_drive_luts_path_text_box", full_path)

        # ✅ Click correct button
        click_button(window, "Write Drive LUTs")

        logger.info("LUT updated successfully.")

    except Exception as exc:
        logger.exception(f"Automation failed: {exc}")
        raise


def Galvo_LUT_Swap() -> None:
    """Main automation workflow."""
    try:
        # launch_application(EXECUTABLE_PATH, WORKING_DIRECTORY)

        app = connect_to_application(EXECUTABLE_PATH)
        window = app.top_window()

        time.sleep(2)

        click_button(window, "Swap VH Drive LUTs")
        time.sleep(2)

        logger.info("Swap LUTs successfully.")

    except Exception as exc:
        logger.exception(f"Swap Failed failed: {exc}")
        raise


# uv run python dump_object_identifiers.py
# exit()
# python -i Launch_CapApp.py
# app, window = debug_setup()

