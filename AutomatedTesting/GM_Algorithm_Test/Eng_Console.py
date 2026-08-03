import subprocess
import time
import pyautogui
import ctypes


# --------------------------
# Caps Lock Helpers
# --------------------------
def capslock_state():
    return ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 1


def capslock_on():
    if capslock_state() == 0:
        pyautogui.press("capslock")


def capslock_off():
    if capslock_state() == 1:
        pyautogui.press("capslock")


# --------------------------
# Main Function
# --------------------------
def cycle_ecs():
    # 1. Launch EngConsole (CMD shortcut)
    subprocess.Popen(
        # r'"C:\Users\Public\Desktop\EngConsole.lnk"',
        r'"C:\Users\ServiceAdmin\Desktop\EngConsole.lnk"',
        shell=True
    )
    # 2. Wait for it to appear
    time.sleep(1.7)

    # 3. Ensure caps is OFF initially
    capslock_off()
    time.sleep(0.5)

    # 4. MAXIMIZE the window (very important)
    pyautogui.hotkey("win", "up")
    time.sleep(0.5)

    # 5. CLICK inside the window (guarantee focus)
    pyautogui.moveTo(500, 500, duration=0.2)
    pyautogui.click()
    time.sleep(0.3)

    # --------------------------
    # 6. Send command sequence
    # --------------------------

    pyautogui.write("k")
    pyautogui.write("i")
    pyautogui.write("0")
    pyautogui.press("enter")

    time.sleep(1)

    pyautogui.write("i")
    pyautogui.write("1")
    pyautogui.press("enter")

    time.sleep(1)

    # 7. Send capital Q (via caps lock)
    capslock_on()
    time.sleep(0.3)

    pyautogui.write("q")

    time.sleep(0.5)
    capslock_off()


# --------------------------
# Run
# --------------------------
if __name__ == "__main__":
    cycle_ecs()
