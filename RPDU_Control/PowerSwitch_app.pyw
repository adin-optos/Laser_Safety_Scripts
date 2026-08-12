"""
App help user to perform the following actions with the network powerswitches
    - select a scan-head
    - Turn Off the switch
    - Turn On the switch
    - check the switch status
    - cycle the switch with a set delay in between off/on
    - soak cycle the switch with configurable number of cycles and delays in between

Switch details from:
https://confluence.optos.eye/display/HWC/Indy+Hardware+booking+sheet
https://confluence.optos.eye/display/HWC/Monaco+Hardware+booking+sheet
https://confluence.optos.eye/display/Verification/Verification+Systems
https://confluence.optos.eye/display/SYSD/Systems+for+DV

Switch manual:
https://gzhls.at/blob/ldb/5/b/3/a/8f525e3e42078b6438b99d3af10e65203135.pdf

To build script as exe
    - (if not already installed) pip install pyinstaller
    - Perhaps best move PowerSwitch_app.py somewhere else to avoid cluttering the repo
        - run "pyinstaller PowerSwitch_app.spec" from cmd
        - grab exe from ./dist/
"""
import json
import os
import re
import sys
import telnetlib
import time
import tkinter as tk
from tkinter.ttk import Combobox
from typing import List

# Variables
window = tk.Tk()
status_lut = {"unknown": "orange", "error": "blue", "ON": "green", "OFF": "red"}
device_status = "unknown"
default_delay = tk.StringVar(value="10")
default_cycles = tk.StringVar(value="1")
default_off = tk.StringVar(value="120")
default_on = tk.StringVar(value="300")
status_text = tk.StringVar(value="App Successfully started")
iconfile = "app.ico"
dynamic_switch_info_file_name = "PowerSwitchList.json"


class RemotePowerSwitchAccessor:
    def __init__(self, ip: str, user: str, password: str) -> None:
        self.ip: str = ip
        self.user: str = user
        self.password: str = password

    def __enter__(self) -> "RemotePowerSwitchAccessor":
        """ Entry point of "with" """
        self.logon()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit point of "with" """
        self.logoff()

    def logon(self) -> None:
        """ Do logon """
        self.session = telnetlib.Telnet(self.ip, "23")
        self.session.read_until(b"User Name :")
        self._send_packet(self.user)
        self.session.read_until(b"Password  :")
        self._send_packet(self.password)
        self.session.read_until(b"apc>")  # Flush the buffer

    def logoff(self) -> None:
        """ Do logoff """
        self._send_packet("bye")

    def send_command(self, com: str) -> str:
        """ Send a single command to switch and get result """
        self._send_packet(com)
        return (self.session.read_until(b"apc>")).decode("ascii")

    def _send_packet(self, data: str) -> None:
        """ Send a single packet to switch """
        self.session.write(data.encode("ascii") + b"\r\n")


# For pyinstaller temp location
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# functions
def powerswitch_handler(action=None):
    """
    Perform the power switch action on the switch at "sys_cb"
    :param action: <str> olon or oloff
    :return: None
    """
    remote_host = systems_lut[sys_cb.get()][0]
    port = systems_lut[sys_cb.get()][3]
    username = systems_lut[sys_cb.get()][1]
    password = systems_lut[sys_cb.get()][2]
    if sys_cb.get() == "00 Custom":
        if custom_ip_tb.get():
            details = custom_ip_tb.get().split(",")
            remote_host = details[0]
            port = details[1]
        custom_ip_tb.delete(0, tk.END)
        custom_ip_tb.insert(0, f"{remote_host},{port}")

    action_cmd = f"{action} {port}"
    status_cmd = f"olStatus {port}"
    name_cmd = f"olName {port}"
    status = "unknown"
    print(f"Checking {remote_host} at PORT: {port} on {remote_host}")

    try:
        with RemotePowerSwitchAccessor(remote_host, username, password) as accessor:
            # ON/OFF
            if action is not None:
                accessor.send_command(action_cmd)
                time.sleep(1)
            # Get current switch status
            reply = accessor.send_command(status_cmd)
            name = accessor.send_command(name_cmd)
            name = re.search(f" {port}: (.+)\\r\\n", name).group(1)
            status_text.set(f"Switch: {remote_host} #{port}  Name: '{name}'")
    except Exception as e:
        print(f"Error: {e}\n")
        status_text.set(f"Switch: {remote_host} #: {port}; {e}")
        return "error"

    if "Success" in reply:
        if "On" in reply:
            status = "ON"
        if "Off" in reply:
            status = "OFF"
    else:
        status = "error"

    return status


def refresh_action():
    """
    Check the switch status, ON or OFF expected
    :return: None
    """
    change_buttons_state(state="disabled")
    window.update()
    if sys_cb.get() == "00 Custom":
        window.geometry("312x140")
    else:
        window.geometry("312x119")

    device_status = powerswitch_handler()
    Status_box.config(text=device_status)
    Status_box.config(bg=status_lut[device_status])

    if device_status in ["ON", "OFF"]:
        change_buttons_state(state="normal")
    refresh_btn.config(text="Refresh")


def on_action():
    """
    Turn the switch on
    :return: None
    """
    device_status = powerswitch_handler("olon")
    Status_box.config(text=device_status)
    Status_box.config(bg=status_lut[device_status])
    if device_status in ["error", "unknown"]:
        change_buttons_state(state="disabled")


def off_action():
    """
    Turn the switch off
    :return: None
    """
    device_status = powerswitch_handler("oloff")
    Status_box.config(text=device_status)
    Status_box.config(bg=status_lut[device_status])
    if device_status in ["error", "unknown"]:
        change_buttons_state(state="disabled")


def single_cycle_action():
    """
    Cycle the switch with time delay from "delay_tb"
    :return: None
    """
    delay = int(delay_tb.get())
    change_buttons_state(state="disabled")
    off_action()
    refresh_btn.config(text="Stop!!!!")

    for time_left in range(delay - 1, -1, -1):
        default_delay.set(time_left)
        window.update()
        time.sleep(1)
        if str(sys_cb.cget("state")) != "disabled":
            default_delay.set(delay)
            refresh_action()
            return

    default_delay.set(delay)
    on_action()
    time.sleep(1)
    refresh_action()


def soak_action():
    """
    Perform soak test with the sys with configurable number of cycles
    and time delays
    :return: Nona
    """
    cyles = int(cyles_tb.get())
    off_period = int(off_cyles_tb.get())
    on_period = int(on_cyles_tb.get())
    change_buttons_state(state="disabled")
    refresh_btn.config(text="Stop!!!!")

    for remaining in range(cyles - 1, -1, -1):
        default_cycles.set(remaining + 1)
        off_action()
        for time_left in range(off_period, -1, -1):
            default_off.set(time_left)
            window.update()
            time.sleep(1)
            if str(sys_cb.cget("state")) != "disabled":
                default_off.set(off_period)
                default_cycles.set(cyles)
                refresh_action()
                window.update()
                return

        default_off.set(off_period)
        window.update()

        on_action()
        for time_left in range(on_period, -1, -1):
            default_on.set(time_left)
            window.update()
            time.sleep(1)
            if str(sys_cb.cget("state")) != "disabled":
                default_on.set(on_period)
                default_cycles.set(cyles)
                refresh_action()
                window.update()
                return

        default_on.set(on_period)
        window.update()

    default_cycles.set(cyles)
    refresh_action()


def change_buttons_state(state="disabled"):
    for bt in [on_btn, off_btn, cycle_btn, soak_btn, sys_cb]:
        bt.configure(state=state)


def load_port_names(switch_ip, user, password) -> List:
    """ Load all port info from specified switch """
    with RemotePowerSwitchAccessor(switch_ip, user, password) as accessor:
        ports = accessor.send_command("olName all")
    # Extract port names and numbers
    reg_ptn = re.compile(r" ([0-9]): (.+)")
    extracted_ports = []
    for port in ports.split("\r\n"):
        matched = reg_ptn.match(port)
        if matched:
            port_num = matched.group(1)
            port_name = matched.group(2)
            extracted_ports.append((port_name, [switch_ip, user, password, port_num]))
    return extracted_ports


def load_switch_data(path) -> dict:
    """ Gather switch spec info via network """
    conf_txt = ""
    with open(path) as file:
        conf_txt = file.read()
    conf_data = json.loads(conf_txt)
    switch_list = conf_data["switch_list"]
    # Gather all switch port info
    candidates = []
    for switch in switch_list:
        try:
            loaded_ports = load_port_names(switch["ip"], switch["user"], switch["pass"])
        except Exception:
            print(f"Failed to fetch port list from {switch['ip']}")
            continue
        candidates.extend(loaded_ports)
    # Exclude items
    exclude_keywords = conf_data["exclude_port_keywords"]
    found_items: dict = {}
    for candidate in candidates:
        port_name, port_spec = candidate
        if not any(key for key in exclude_keywords if key in port_name.lower()):
            found_items[port_name] = port_spec
    # Setup pulldown list source
    return found_items


if __name__ == "__main__":
    # Load switch info via network
    print("Loading switch info from network...")
    if os.path.exists(dynamic_switch_info_file_name):
        systems_lut = load_switch_data(dynamic_switch_info_file_name)
    else:
        systems_lut = load_switch_data(resource_path(dynamic_switch_info_file_name))

    systems_lut.update({"00 Custom": ["172.20.23.234", "OptosService", "R-?A0#1Rx9n)+mD9Y9CBcB4F", "8"]})

    # All GUI stuff lay out details and main program
    # 1st row
    sys_cb = Combobox(
        window, values=sorted(systems_lut.keys(), key=str.lower), height=35, width=25
    )
    sys_cb.bind("<<ComboboxSelected>>", lambda event: refresh_action())
    sys_cb.place(x=10, y=13)

    refresh_btn = tk.Button(window, text="Refresh", fg="blue", command=refresh_action)
    refresh_btn.place(x=188, y=10)

    Status_box = tk.Label(window, text=device_status, bg="orange", fg="white")
    Status_box.place(x=248, y=13)

    # 2nd row
    on_btn = tk.Button(window, text="ON", fg="Green", command=on_action)
    on_btn.place(x=10, y=40)

    off_btn = tk.Button(window, text="OFF", fg="Red", command=off_action)
    off_btn.place(x=50, y=40)

    cycle_btn = tk.Button(
        window, text="OFF/ON", fg="Orange", command=single_cycle_action
    )
    cycle_btn.place(x=90, y=40)

    delay_label = tk.Label(window, text="time delay (s):")
    delay_label.place(x=150, y=45)

    delay_tb = tk.Entry(window, textvariable=default_delay, width=3)
    delay_tb.place(x=240, y=45)

    # 3rd row
    soak_btn = tk.Button(window, text="SOAK", fg="orange", command=soak_action)
    soak_btn.place(x=10, y=70)

    soak_label = tk.Label(window, text="cycles")
    soak_label.place(x=50, y=75)

    cyles_tb = tk.Entry(window, textvariable=default_cycles, width=3)
    cyles_tb.place(x=90, y=75)

    off_soak_label = tk.Label(window, text="OFF delay")
    off_soak_label.place(x=110, y=75)

    off_cyles_tb = tk.Entry(window, textvariable=default_off, width=3)
    off_cyles_tb.place(x=170, y=75)

    on_soak_label = tk.Label(window, text="ON delay")
    on_soak_label.place(x=195, y=75)

    on_cyles_tb = tk.Entry(window, textvariable=default_on, width=4)
    on_cyles_tb.place(x=250, y=75)

    custom_ip_text = tk.Label(window, text="Custom Powerswitch (ip , port)")
    custom_ip_text.place(x=10, y=100)

    # custom_ip_tb = tk.Entry(window, textvariable=default_ip, width=15)
    custom_ip_tb = tk.Entry(window, width=15)
    custom_ip_tb.place(x=180, y=100)

    statusbar = tk.Label(
        window, textvariable=status_text, bd=1, relief=tk.SUNKEN, anchor=tk.W
    )
    statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    change_buttons_state()
    sys_cb.configure(state="normal")
    window.title("Power Switch App")
    window.geometry("312x119")
    window.iconbitmap(default=resource_path(iconfile))
    window.mainloop()
