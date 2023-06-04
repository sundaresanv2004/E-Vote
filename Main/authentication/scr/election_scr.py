import pandas as pd

from Main.authentication.files.write_files import new_election_creation
from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path
from Main.functions.date_time import present_year

election_data = pd.read_csv(path + file_path["election_data"])
current_election_path = election_data.values[0][1]


def election_start_scr():
    global current_election_path
    election_data = pd.read_csv(path + file_path["election_data"])
    settings_df = pd.read_json(path + file_path['settings'], orient='table')
    if election_data.empty is True:
        new_election_creation(f"{present_year}-Election")
        election_start_scr()
    else:
        current_election_path = election_data[election_data.name == settings_df.loc['Election'].values[0]].values[0][1]
