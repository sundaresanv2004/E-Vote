import pandas as pd

from ..scr.check_installation import path
from ..scr.loc_file_scr import file_path
from ...functions.dialogs import loading_dialogs
from ...functions.snack_bar import snack_bar1


def window_resize_change(val):
    ser1 = pd.read_json(path + file_path['settings'], orient='table')
    ser1.loc['maximized'].values[0] = val
    ser1.to_json(path + file_path['settings'], orient='table', index=True)


def main_theme_on_change(val):
    ser1 = pd.read_json(path + file_path['settings'], orient='table')
    ser1.loc['Theme Mode'].values[0] = val
    ser1.to_json(path + file_path['settings'], orient='table', index=True)


def institution_name_change(name: str):
    app_data_sys_df1 = pd.read_json(path + file_path['app_data'], orient='table')
    app_data_sys_df1.at[1, 'values'] = name
    app_data_sys_df1.to_json(path + file_path['app_data'], orient='table', index=False)
    from ...pages.settings import update_settings_data
    update_settings_data()


def current_election_name(name: str, page):
    settings_df2 = pd.read_json(path + file_path['settings'], orient='table')
    settings_df2.loc['Election'] = name
    settings_df2.to_json(path + file_path['settings'], orient='table', index=True)
    loading_dialogs(page, "Changing...", 2)
    snack_bar1(page, "Successfully Changed.")
    from ...pages.settings import update_settings_data
    update_settings_data()
    from ..scr.election_scr import election_start_scr
    election_start_scr()

