import pandas as pd

from .loc_file_scr import file_path
from ..scr.check_installation import path

election_data = pd.read_csv(path + file_path["election_data"])
current_election_path = election_data.values[0][1]


def election_start_scr():
    global current_election_path
    election_data1 = pd.read_csv(path + file_path["election_data"])
    settings_df = pd.read_json(path + file_path['settings'], orient='table')
    if pd.isna(settings_df.loc['Election'].values[0]) is True:
        settings_df.loc['Election'] = election_data1.loc[0].values[0]
        settings_df.to_json(path + file_path['settings'], orient='table', index=True)
        election_start_scr()
    else:
        current_election_path = election_data1[election_data1.name == settings_df.loc['Election'].values[0]].values[0][1]
