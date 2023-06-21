import flet as ft
import pandas as pd

from ..functions.window_close import close_true
from ..service.files.settings_write import window_resize_change
from ..service.scr.check_installation import path
from ..service.scr.loc_file_scr import file_path


def window_at_start(page: ft.Page):
    ser1 = pd.read_json(path + file_path['settings'], orient='table')

    # at_close
    def at_close_event(e):
        if e.data == "close":
            close_true(page)

    # ask question at close [True, False]
    page.window_prevent_close = ser1.loc['close'].values[0]
    page.on_window_event = at_close_event

    page.window_maximized = ser1.loc['maximized'].values[0]


def window_on_resize(page: ft.Page):
    try:
        ser1 = pd.read_json(path + file_path['settings'], orient='table')
        if page.window_maximized != ser1.loc['maximized'].values[0]:
            window_resize_change(page.window_maximized)
        page.update()
    except ValueError:
        pass
