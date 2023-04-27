import flet as ft
import pandas as pd

from ..authentication.files.settings_write import window_resize_change
from ..authentication.scr.check_installation import path
from ..authentication.scr.loc_file_scr import file_path


def window_size_at_start(page: ft.Page):
    ser1 = pd.read_json(path + file_path['settings'], orient='table')
    page.window_maximized = ser1.loc['maximized'].values[0]


def window_maximized(page: ft.Page):
    ser1 = pd.read_json(path + file_path['settings'], orient='table')

    if page.window_maximized != ser1.loc['maximized'].values[0]:
        window_resize_change(page.window_maximized)
