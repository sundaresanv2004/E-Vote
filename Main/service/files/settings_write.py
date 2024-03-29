import shutil
import numpy as np
import pandas as pd

from ..scr.check_installation import path
from ..scr.loc_file_scr import file_path, file_data
import Main.service.scr.election_scr as ee
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
    from ..scr.election_scr import election_start_scr
    election_start_scr()
    from ...pages.settings import update_settings_data
    update_settings_data()


def delete_election():
    election_data01 = pd.read_csv(path + file_path["election_data"])
    settings_df = pd.read_json(path + file_path['settings'], orient='table')

    election_index = election_data01[election_data01.name == settings_df.loc['Election'].values[0]].index.values[0]
    election_dir = election_data01[election_data01.name == settings_df.loc['Election'].values[0]].values[0][1]

    election_data01.drop(election_index, axis=0, inplace=True)
    settings_df.loc['Election'] = np.NaN
    settings_df.to_json(path + file_path['settings'], orient='table', index=True)
    try:
        shutil.rmtree(election_dir)
    except OSError:
        pass

    election_data01.to_csv(path + file_path["election_data"], index=False)


def change_election_name(title):
    ele_ser = pd.read_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table')
    election_data = pd.read_csv(path + file_path["election_data"])
    settings_df = pd.read_json(path + file_path['settings'], orient='table')
    index_val = election_data[election_data.name == ele_ser.loc['election-name'].values[0]].index.values[0]
    election_data.at[index_val, 'name'] = title
    settings_df.loc['Election'] = title
    ele_ser.loc['election-name'] = title
    ele_ser.to_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table', index=True)
    settings_df.to_json(path + file_path['settings'], orient='table', index=True)
    election_data.to_csv(path + file_path["election_data"], index=False)
    from ...pages.settings import update_settings_data
    update_settings_data()
