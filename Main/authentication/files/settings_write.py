import pandas as pd

import Main.authentication.scr.election_scr as ee
from ..encrypter.encryption import encrypter
from ..scr.check_installation import path
from ..scr.loc_file_scr import file_data, file_path
from ...pages.settings_home import from_page_check


def registration(val):
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    if val is True:
        ele_ser.loc['registration'] = True
    else:
        ele_ser.loc['registration'] = False
    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    from_page_check()


def registration_date(from_val, to_val):
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    ele_ser.loc['registration_from'] = from_val
    ele_ser.loc['registration_to'] = to_val
    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    from_page_check()


def change_election_name(title):
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    election_data = pd.read_csv(path + file_path["election_data"])
    settings_df = pd.read_json(path + file_path['settings'], orient='table')
    index_val = election_data[election_data.name == ele_ser.loc['election-name'].values[0]].index.values[0]
    election_data.at[index_val, 'name'] = title
    settings_df.loc['Election'] = title
    ele_ser.loc['election-name'] = title
    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    settings_df.to_json(path + file_path['settings'], orient='table', index=True)
    election_data.to_csv(path + file_path["election_data"], index=False)
    from_page_check()


def first_lock(data):
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    ele_ser.loc['code'] = encrypter(data)
    ele_ser.loc['registration'] = False
    ele_ser.loc['lock_data'] = True
    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    from_page_check()


def lock_and_unlock():
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    if ele_ser.loc['lock_data'].values[0]:
        ele_ser.loc['lock_data'] = False
    else:
        ele_ser.loc['lock_data'] = True
        ele_ser.loc['registration'] = False

    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    from_page_check()
