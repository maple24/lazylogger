import PySimpleGUI as sg
import os
from loguru import logger
import threading
import time
from SystemHelper import SystemHelper
from GenericHelper import GenericHelper
from utils import (
    strip_ansi_escape_codes,
    load_value_from_shelf,
    save_value_to_shelf,
    get_file_modification_times,
    get_desktop,
    list_files,
)

# ========================================prepare================================================
# ========================================prepare================================================
sg.theme("Topanga")  # Use the 'Topanga' theme for a colorful appearance
__author__ = "Author: ZHU JIN"
__version__ = "Version: 1.0"


# Configure Loguru to use the custom handler
def gui_log_handler(message):
    clean_message = strip_ansi_escape_codes(message)
    window["log"].update(value=clean_message, append=True)


def set_defaults(input_value):
    if deviceid := SystemHelper.get_adb_devices():
        window["deviceid"].update(deviceid[0])
    window["user"].update(GenericHelper.get_username())
    window["machine"].update(GenericHelper.get_hostname())
    if not input_value:
        return
    if a := input_value.get("aos"):
        window["aos"].update(a)
    if q := input_value.get("qnx"):
        window["qnx"].update(q)
    if u := input_value.get("username"):
        window["username"].update(u)
    if p := input_value.get("password"):
        window["password"].update(p)
    if c := input_value.get("comport"):
        window["comport"].update(c)
    if f := input_value.get("folder"):
        window["folder"].update(f)
    if qm := input_value.get("qnxmapping"):
        window["qnxmapping"].update(qm)
        SystemHelper.disk_mapping.update({"qnx": qm})
    if am := input_value.get("aosmapping"):
        window["aosmapping"].update(am)
        SystemHelper.disk_mapping.update({"android": am})


def update_text_area(default_folder):
    previous_mod_times = get_file_modification_times(default_folder)

    while True:
        time.sleep(0.1)
        folder_path = window["folder"].get()
        current_mod_times = get_file_modification_times(folder_path)
        changed_files = [
            file
            for file in current_mod_times
            if current_mod_times[file] != previous_mod_times.get(file)
        ]
        if changed_files:
            window["output"].update("\n".join(changed_files))
        previous_mod_times = current_mod_times
        sg.popup_animated(None)  # Refresh the window to prevent flickering


logger.remove()  # Remove the default logger
logger.add(gui_log_handler, colorize=True)  # Add the custom handler
default_folder = get_desktop()
# ========================================prepare================================================
# ========================================prepare================================================

# *********************************************layouts*********************************************
# *********************************************layouts*********************************************
software_frame = [
    [sg.Text(__author__), sg.Text(__version__)],
    [sg.HorizontalSeparator()],
    [
        sg.Text("User", size=(15,)),
        sg.InputText(default_text="", key="user", size=(20,)),
    ],
    [
        sg.Text("Machine", size=(15,)),
        sg.InputText(default_text="", key="machine", size=(20,)),
    ],
]
system_frame = [
    [
        sg.Text("Username", size=(15,)),
        sg.InputText(default_text="zeekr", key="username", size=(20,)),
    ],
    [
        sg.Text("Password", size=(15,)),
        sg.InputText(default_text="Aa123123", key="password", size=(20,)),
    ],
    [
        sg.Text("Comport", size=(15,)),
        sg.InputText(key="comport", size=(20,)),
    ],
    [
        sg.Text("DeviceID", size=(15,)),
        sg.InputText(key="deviceid", size=(20,)),
    ],
    [
        sg.Text("QNX_mapping", size=(15,)),
        sg.InputText(default_text="/mnt/nfs_share", key="qnxmapping", size=(20,)),
    ],
    [
        sg.Text("AOS_mapping", size=(15,)),
        sg.InputText(default_text="/nfs_share", key="aosmapping", size=(20,)),
    ],
]
input_frame = [
    [sg.Text("Local path: ")],
    [
        sg.InputText(
            key="folder",
            size=(60,),
            default_text=default_folder,
            text_color="black",
            disabled=True,
            enable_events=True,
        ),
        sg.FolderBrowse("Browse", initial_folder=default_folder),
    ],
    [sg.Text("QNX path: ")],
    [sg.InputText(key="qnx", size=(60,), focus=True)],
    [sg.Text("eg. /mnt/nfs_share/test.txt", font=("Arial", 8))],
    [sg.Text("Android path: ")],
    [sg.InputText(key="aos", size=(60,)), sg.Button("Execute")],
    [sg.Text("eg. /data/vendor/nfs/mount/text.txt", font=("Arial", 8))],
]
magic_frame = [
    # [sg.Button("Clear")],
    [sg.Button("Android_Snapshot")],
    [sg.Button("Android_Logcat")],
    [sg.Button("Android_Anr")],
    [sg.Button("Android_Tombstones")],
    [sg.Button("QNX_slog2info")],
]
output_frame = [
    [
        sg.Multiline(
            key="log", size=(100, 10), background_color="black", autoscroll=True
        )
    ],
    [
        sg.Multiline(
            key="output", size=(100, 5), background_color="black", autoscroll=True
        )
    ],
]

# Combine frames and separator in the layout
layout = [
    [
        sg.Frame("Software", software_frame, font=("Arial", 12), size=(350, 180)),
        sg.VerticalSeparator(),
        sg.Frame("System", system_frame, font=("Arial", 12), size=(350, 180)),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Frame("Input", input_frame, font=("Arial", 12), size=(500, 240)),
        sg.VerticalSeparator(),
        sg.Frame("Magic", magic_frame, font=("Arial", 12), size=(200, 240)),
    ],
    [sg.HorizontalSeparator()],
    [sg.Frame("Output", output_frame, font=("Arial", 12))],
]
# *********************************************layouts*********************************************
# *********************************************layouts*********************************************

window = sg.Window("Lazy Logger", layout, finalize=True)
window["qnx"].bind("<Return>", "_Enter")  # Bind the Return key to the Execute button
window["aos"].bind("<Return>", "_Enter")  # Bind the Return key to the Execute button
store = load_value_from_shelf()
input_value = store if store else {}
threading.Thread(target=set_defaults, args=(input_value,), daemon=True).start()
threading.Thread(target=update_text_area, args=(default_folder,), daemon=True).start()

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        input_value.update(
            {
                "aos": window["aos"].get(),
                "qnx": window["qnx"].get(),
                "username": window["username"].get(),
                "password": window["password"].get(),
                "comport": window["comport"].get(),
                "folder": window["folder"].get(),
                "qnxmapping": window["qnxmapping"].get(),
                "aosmapping": window["aosmapping"].get(),
            }
        )
        save_value_to_shelf(input_value)
        break
    elif event == "Execute" or event == "qnx_Enter" or event == "aos_Enter":
        if aos_path := values["aos"]:
            threading.Thread(
                target=SystemHelper.Android2PC,
                kwargs={
                    "androidPath": aos_path,
                    "localPath": values["folder"],
                    "deviceID": values["deviceid"],
                },
                daemon=True,
            ).start()
        if qnx_path := values["qnx"]:
            threading.Thread(
                target=SystemHelper.QNX2PC,
                kwargs={
                    "comport": values["comport"],
                    "qnxPath": qnx_path,
                    "localPath": values["folder"],
                    "deviceID": values["deviceid"],
                    "username": values["username"],
                    "password": values["password"],
                },
                daemon=True,
            ).start()
    elif event == "Android_Snapshot":
        threading.Thread(
            target=SystemHelper.android_screencapture,
            kwargs={
                "deviceID": values["deviceid"],
                "localPath": values["folder"],
            },
            daemon=True,
        ).start()
    elif event == "Android_Logcat":
        threading.Thread(
            target=SystemHelper.android_logcat,
            kwargs={
                "deviceID": values["deviceid"],
                "localPath": values["folder"],
            },
            daemon=True,
        ).start()
    elif event == "Android_Anr":
        threading.Thread(
            target=SystemHelper.Android2PC,
            kwargs={
                "androidPath": '/data/anr',
                "localPath": values["folder"],
                "deviceID": values["deviceid"],
            },
            daemon=True,
        ).start()
    elif event == "Android_Tombstones":
        threading.Thread(
            target=SystemHelper.Android2PC,
            kwargs={
                "androidPath": '/data/tombstones',
                "localPath": values["folder"],
                "deviceID": values["deviceid"],
            },
            daemon=True,
        ).start()
    elif event == "QNX_slog2info":
        threading.Thread(
            target=SystemHelper.QNX_slog,
            kwargs={
                "comport": values["comport"],
                "localPath": values["folder"],
                "deviceID": values["deviceid"],
                "username": values["username"],
                "password": values["password"],
            },
            daemon=True,
        ).start()
    elif event == "Clear":
        window["log"].update("")
        window["output"].update("")

window.close()
