import datetime
import numpy as np
import pandas as pd

from Main.authentication.encrypter.encryption import encrypter
from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path


def admin_data_in(admin_data_new_in_list: list):
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    staff_login_df = pd.read_json(path + file_path['admin_login_data'], orient='table')

    max_index = staff_df['id'].max()
    if max_index is np.nan:
        max_index = 1
    else:
        max_index += 1

    staff_df.loc[max_index] = [max_index, encrypter(admin_data_new_in_list[0]),
                               encrypter(admin_data_new_in_list[1]),
                               encrypter(admin_data_new_in_list[2]),
                               admin_data_new_in_list[3], 'system', np.nan]
    staff_login_df.loc[max_index] = [max_index, False, False]
    staff_df.to_json(path + file_path['admin_data'], orient='table', index=False)
    staff_login_df.to_json(path + file_path['admin_login_data'], orient='table', index=False)


def login_details_update(index_val):
    staff_login_df = pd.read_json(path + file_path['admin_login_data'], orient='table')
    staff_login_df.at[index_val, 'date'] = datetime.date.today()
    staff_login_df.at[index_val, 'time'] = datetime.datetime.now().strftime("%H:%M:%S")
    staff_login_df.to_json(path + file_path['admin_login_data'], orient='table', index=False)


def new_election_creation(tittle: str):
    from Main.authentication.files.files_cre import new_election_creation_folder

    election_data = pd.read_csv(path + file_path["election_data"])
    settings_df = pd.read_json(path + file_path['settings'], orient='table')

    if election_data.empty is True:
        election_data.loc['0'] = [tittle, path + file_path['candidate_data'] + rf'\{tittle}']
        settings_df.loc['Election'] = tittle
        settings_df.to_json(path + file_path['settings'], orient='table', index=True)

    election_data.to_csv(path + file_path["election_data"], index=False)
    new_election_creation_folder(tittle)


def delete_staff_data(index_df):
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    staff_login_df = pd.read_json(path + file_path['admin_login_data'], orient='table')

    index_val = staff_df[staff_df.id == index_df].index.values[0]
    staff_df1 = staff_df.drop(index_val, axis=0)
    staff_login_df1 = staff_login_df.drop(index_val, axis=0)

    staff_df1.to_json(path + file_path['admin_data'], orient='table', index=False)
    staff_login_df1.to_json(path + file_path['admin_login_data'], orient='table', index=False)


def theme_on_change(theme_mod: str):
    import Main.authentication.user.login_enc as cc
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    index_val = staff_df[staff_df.id == cc.teme_data[0]].index.values[0]
    staff_df.at[index_val, "theme"] = theme_mod

    staff_df.to_json(path + file_path['admin_data'], orient='table', index=False)


def category_add_new(list_data: list):
    from ..scr.loc_file_scr import file_data
    import Main.authentication.scr.election_scr as ee

    category_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')
    index_val = category_df['id'].max()
    print(index_val)
    if index_val is np.nan:
        index_val = 1
    else:
        index_val += 1
