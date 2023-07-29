import numpy as np
import pandas as pd

from Main.service.scr.loc_file_scr import file_data
import Main.service.scr.election_scr as ee

election_data_loc = rf'/{file_data["vote_data"]}/{file_data["election_data"]}'


def generate_result_fun():
    from Main.pages.election_settings import update_election_set
    election_data3 = pd.read_json(ee.current_election_path + election_data_loc, orient='table')
    candidate_df = pd.read_json(
        ee.current_election_path + rf'/{file_data["vote_data"]}/{file_data["final_nomination"]}',
        orient='table')
    final_category_data2 = pd.read_csv(
        ee.current_election_path + rf'/{file_data["vote_data"]}/{file_data["final_category"]}')
    category_list1 = list(final_category_data2['category'])
    temp_df1 = pd.DataFrame(candidate_df[['id', 'candidate_name', 'category', 'qualification', 'image']])
    temp_df1['no_of_votes'] = 0

    for i in category_list1:
        teme_category_list = list(election_data3[i])
        a_ = temp_df1[temp_df1.category == i].values
        for k in range(len(a_)):
            temp_index = temp_df1[temp_df1.id == a_[k][0]].index.values[0]
            temp_df1.at[temp_index, 'no_of_votes'] = teme_category_list.count(a_[k][0])

    temp_df1.to_json(ee.current_election_path + rf'/{file_data["vote_data"]}/{file_data["result"]}',
                     orient='table', index=False)
    update_election_set()
