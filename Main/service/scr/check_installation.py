import platform
import os
import pandas as pd

from .loc_file_scr import file_path, default_setting_data

print(os.path.expanduser('~'))

path = None
os_sys = None
if platform.system() == "Windows":
    os_sys = "Windows"
    path = os.getenv('APPDATA') + r'/E-Vote'
elif platform.system() == 'Darwin':
    os_sys = platform.system()
    path = os.path.expanduser('~') + r"/E-Vote"


def installation_requirement():
    if not os.path.exists(path + file_path['settings']):
        if not os.path.exists(path + r'/data'):
            os.makedirs(path + r'/data')
            os.makedirs(path + r'/data/a')
            os.makedirs(path + r'/data/c')
            os.makedirs(path + r'/data/e')
            os.makedirs(path + r'/data/s')
            os.makedirs(path + r'/backup')
        ser1 = pd.Series(default_setting_data)
        ser1.to_json(path + file_path['settings'], orient='table', index=True)


if not os.path.exists(path + r'/data/s/abxyzc'):
    start = True
else:
    start = False
