import datetime
import os
import numpy as np
import pandas as pd
import string
import random

from ..enc.encryption import encrypter
from ..scr.check_installation import path
from ..scr.loc_file_scr import file_path


def admin_data_in(admin_data_new_in_list: list):
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    staff_login_df = pd.read_json(path + file_path['admin_login_data'], orient='table')

    max_index = staff_df['id'].max()
    if max_index is np.nan:
        max_index = 1
    else:
        max_index += 1

    staff_df.loc['a'] = [max_index, encrypter(admin_data_new_in_list[0]),
                         encrypter(admin_data_new_in_list[1]),
                         encrypter(admin_data_new_in_list[2]),
                         admin_data_new_in_list[3], 'system', np.nan]
    staff_login_df.loc['a'] = [max_index, False, False]
    staff_df.to_json(path + file_path['admin_data'], orient='table', index=False)
    staff_login_df.to_json(path + file_path['admin_login_data'], orient='table', index=False)


def login_details_update(index_val):
    staff_login_df = pd.read_json(path + file_path['admin_login_data'], orient='table')
    staff_login_df.at[index_val, 'date'] = datetime.date.today()
    staff_login_df.at[index_val, 'time'] = datetime.datetime.now().strftime("%H:%M:%S")
    staff_login_df.to_json(path + file_path['admin_login_data'], orient='table', index=False)


def new_election_creation(title: str):
    from .files_cre import new_election_creation_folder

    election_data = pd.read_csv(path + file_path["election_data"])
    source = string.ascii_letters + string.digits
    rand = ''.join((random.choice(source)) for i in range(8))
    folder_name = rand + title
    election_data.loc['a'] = [title, path + file_path['candidate_data'] + rf'\{folder_name}']
    election_data.to_csv(path + file_path["election_data"], index=False)
    new_election_creation_folder(title, folder_name)


def delete_staff_data(index_df):
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    staff_login_df = pd.read_json(path + file_path['admin_login_data'], orient='table')

    index_val = staff_df[staff_df.id == index_df].index.values[0]
    staff_df1 = staff_df.drop(index_val, axis=0)
    staff_login_df1 = staff_login_df.drop(index_val, axis=0)

    staff_df1.to_json(path + file_path['admin_data'], orient='table', index=False)
    staff_login_df1.to_json(path + file_path['admin_login_data'], orient='table', index=False)


def edit_staff_data(data_list: list, index_user):
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')

    index_val = staff_df[staff_df.id == index_user].index.values[0]
    staff_df.at[index_val, 'name'] = encrypter(data_list[0])
    staff_df.at[index_val, 'mail_id'] = encrypter(data_list[1])
    staff_df.at[index_val, 'password'] = encrypter(data_list[2])
    staff_df.at[index_val, 'permission'] = data_list[3]

    staff_df.to_json(path + file_path['admin_data'], orient='table', index=False)


def category_add_new(list_data: list):
    from ..scr.loc_file_scr import file_data
    import Main.service.scr.election_scr as ee

    category_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')
    index_val = category_df['id'].max()

    if index_val is np.nan:
        index_val = 1
    else:
        index_val += 1

    category_df.loc['a'] = [index_val, list_data[0], list_data[1]]
    category_df.to_csv(ee.current_election_path + rf'\{file_data["category_data"]}', index=False)


def add_candidate(list1_data: list):
    from ..scr.loc_file_scr import file_data
    import Main.service.scr.election_scr as ee

    candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')

    index_val = candidate_data_df['id'].max()

    if index_val is np.nan:
        index_val = 1
    else:
        index_val += 1

    candidate_data_df.loc['a'] = [index_val, list1_data[0], list1_data[1], list1_data[2], list1_data[3],
                                  list1_data[4], f'{datetime.date.today()}', list1_data[5]]

    candidate_data_df.to_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table',
                              index=False)


def delete_candidate(index_val):
    from ..scr.loc_file_scr import file_data
    import Main.service.scr.election_scr as ee

    candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')
    user_data = candidate_data_df.loc[index_val].values
    if user_data[5] != False:
        candidate_image_destination = ee.current_election_path + r'\images'
        try:
            os.remove(candidate_image_destination + fr'\{user_data[5]}')
        except FileNotFoundError:
            pass

    candidate_data_df.drop(index_val, axis=0, inplace=True)
    candidate_data_df.to_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table',
                              index=False)


def candidate_edit(list_data: list, index_val):
    from ..scr.loc_file_scr import file_data
    import Main.service.scr.election_scr as ee

    candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')

    candidate_data_df.at[index_val, 'candidate_name'] = list_data[0]
    candidate_data_df.at[index_val, 'category'] = list_data[1]
    candidate_data_df.at[index_val, 'qualification'] = list_data[2]
    if list_data[3] != False:
        candidate_data_df.at[index_val, 'image'] = list_data[3]
    candidate_data_df.to_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table',
                              index=False)


def category_edit(list_data: list, index_val):
    import Main.service.scr.election_scr as ee
    from ..scr.loc_file_scr import file_data

    category_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')
    category_df.loc[index_val, 'category'] = list_data[0]
    category_df.loc[index_val, 'qualification'] = list_data[1]
    category_df.to_csv(ee.current_election_path + rf'\{file_data["category_data"]}', index=False)


def delete_category(index_val):
    import Main.service.scr.election_scr as ee
    from ..scr.loc_file_scr import file_data

    category_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')
    category_df.drop(index_val, axis=0, inplace=True)
    category_df.to_csv(ee.current_election_path + rf'\{file_data["category_data"]}', index=False)
