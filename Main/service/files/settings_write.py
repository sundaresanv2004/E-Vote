import pandas as pd

from ..scr.check_installation import path
from ..scr.loc_file_scr import file_path


def window_resize_change(val):
    ser1 = pd.read_json(path + file_path['settings'], orient='table')
    ser1.loc['maximized'].values[0] = val
    ser1.to_json(path + file_path['settings'], orient='table', index=True)


def main_theme_on_change(val):
    ser1 = pd.read_json(path + file_path['settings'], orient='table')
    ser1.loc['Theme Mode'].values[0] = val
    ser1.to_json(path + file_path['settings'], orient='table', index=True)
