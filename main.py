import PySimpleGUI as sg
from loguru import logger
from SystemHelper import SystemHelper
from GenericHelper import GenericHelper
from utils import strip_ansi_escape_codes, load_value_from_shelf, save_value_to_shelf

# ========================================================================================
gHelper = GenericHelper()
sHelper = SystemHelper()
sg.theme("Topanga")  # Use the 'Topanga' theme for a colorful appearance


# Configure Loguru to use the custom handler
def gui_log_handler(message):
    clean_message = strip_ansi_escape_codes(message)
    window["log"].update(value=clean_message, append=True)


def set_defaults(input_value):
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
    window["deviceid"].update("test")


logger.remove()  # Remove the default logger
logger.add(gui_log_handler, colorize=True)  # Add the custom handler
# ========================================================================================

# *********************************************layouts*********************************************
user_frame = [
    [
        sg.Text("User", size=(10,)),
        sg.InputText(default_text="", key="user", size=(20,)),
    ],
]
system_frame = [
    [
        sg.Text("Username", size=(10,)),
        sg.InputText(default_text="zeekr", key="username", size=(20,)),
    ],
    [
        sg.Text("Password", size=(10,)),
        sg.InputText(default_text="Aa123123", key="password", size=(20,)),
    ],
    [
        sg.Text("Comport", size=(10,)),
        sg.InputText(key="comport", size=(20,)),
    ],
    [
        sg.Text("DeviceID", size=(10,)),
        sg.InputText(key="deviceid", size=(20,)),
    ],
]
input_frame = [
    [sg.Text("QNX path: ")],
    [sg.InputText(key="qnx", size=(52,), focus=True)],
    [sg.Text("eg. /mnt/nfs_share/test.txt", font=("Arial", 8))],
    [sg.Text("Android path: ")],
    [sg.InputText(key="aos", size=(52,)), sg.Button("Execute")],
    [sg.Text("eg. /data/vendor/nfs/mount/text.txt", font=("Arial", 8))],
]
magic_frame = [
    # [sg.Button("Clear")],
    [sg.Button("Android_Snapshot")],
    [sg.Button("Android_Logcat")],
    [sg.Button("QNX_slog2info")],
]

output_frame = [
    [sg.Multiline(key="log", size=(100, 10), background_color="black")],
    [sg.Multiline(key="output", size=(100, 10), background_color="black")],
]

# Combine frames and separator in the layout
layout = [
    [
        sg.Frame("User", user_frame, font=("Arial", 12), size=(350, 150)),
        sg.VerticalSeparator(),
        sg.Frame("System", system_frame, font=("Arial", 12), size=(350, 150)),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Frame("Input", input_frame, font=("Arial", 12), size=(500, 180)),
        sg.VerticalSeparator(),
        sg.Frame("Magic", magic_frame, font=("Arial", 12), size=(200, 180)),
    ],
    [sg.HorizontalSeparator()],
    [sg.Frame("Output", output_frame, font=("Arial", 12))],
]
# *********************************************layouts*********************************************

window = sg.Window("Lazy Logger", layout, finalize=True)
window["qnx"].bind("<Return>", "_Enter")  # Bind the Return key to the Execute button
window["aos"].bind("<Return>", "_Enter")  # Bind the Return key to the Execute button
input_value = load_value_from_shelf()
set_defaults(input_value)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        input_value.update({
            "aos": window["aos"].get(),
            "qnx": window["qnx"].get(),
            "username": window["username"].get(),
            "password": window["password"].get(),
            "comport": window["comport"].get(),
        })
        save_value_to_shelf(input_value)
        break
    elif event == "Execute" or event == "qnx_Enter" or event == "aos_Enter":
        qnx_path = values["qnx"]
        aos_path = values["aos"]
        # if aos_path:
        #     sHelper.Android2PC(androidPath=aos_path)
        # if qnx_path:
        #     sHelper.QNX2PC()
        # output_text = f"Command: {output}\nOutput: [Output will go here]\n"
        # window["output"].print(output_text)
    elif event == "Android_Snapshot":
        ...
    elif event == "Android_Logcat":
        ...
    elif event == "QNX_slog2info":
        ...
    elif event == "Clear":
        window["log"].update("")
        window["output"].update("")

window.close()
