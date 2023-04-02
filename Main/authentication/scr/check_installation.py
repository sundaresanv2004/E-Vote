import platform
import os
import pandas as pd

from Main.authentication.scr.loc_file_scr import file_path, default_setting_data


path = None
os_sys = None
if platform.system() == "Windows":
    os_sys = "Windows"
    path = os.getenv('APPDATA') + r'\E Vote'
else:
    os_sys = platform.system()


def installation_requirement():
    if not os.path.exists(path + file_path['settings']):
        if not os.path.exists(path):
            os.makedirs(path + r'\assets')
            os.makedirs(path + r'\assets\a')
            os.makedirs(path + r'\assets\c')
            os.makedirs(path + r'\assets\e')
            os.makedirs(path + r'\assets\s')
            os.makedirs(path + r'\backup')
            os.makedirs(path + r'\versions')
        ser1 = pd.Series(default_setting_data)
        ser1.to_json(path + file_path['settings'], orient='table', index=True)


if not os.path.exists(path + r'\assets\s\abxyzc'):
    start = True
else:
    start = False
