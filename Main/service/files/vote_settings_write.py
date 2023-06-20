import pandas as pd

import Main.service.scr.election_scr as ee
from ..enc.encryption import encrypter
from ..scr.loc_file_scr import file_data
from ...pages.election_settings import update_election_set


def first_lock(data):
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    ele_ser.loc['code'] = encrypter(data)
    ele_ser.loc['registration'] = False
    ele_ser.loc['lock_data'] = True
    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    update_election_set()


def lock_and_unlock():
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    if ele_ser.loc['lock_data'].values[0]:
        ele_ser.loc['lock_data'] = False
        ele_ser.loc['vote'] = False
    else:
        ele_ser.loc['lock_data'] = True
        ele_ser.loc['registration'] = False

    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    update_election_set()


def final_list(list_data):
    candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')
    df1 = candidate_data_df[candidate_data_df.verification == True]
    df1.reset_index(inplace=True, drop=True)
    df2 = pd.DataFrame(columns=df1.columns.values)
    for i in range(len(df1)):
        if df1.loc[i]['category'] in list_data:
            df2.loc[i] = df1.loc[i].values
    df2.reset_index(inplace=True, drop=True)
    df2['id'] = df2.index.values + 1

    category_df = pd.DataFrame(columns=['id', 'category'])
    for i in range(len(list_data)):
        category_df.loc[i] = [i + 1, list_data[i]]

    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    ele_ser.loc['final_nomination'] = True

    df2.to_json(ee.current_election_path + rf'\{file_data["vote_data"]}\{file_data["final_nomination"]}',
                orient='table', index=False)
    category_df.to_csv(ee.current_election_path + rf'\{file_data["vote_data"]}\{file_data["final_category"]}',
                       index=False)
    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    update_election_set()
