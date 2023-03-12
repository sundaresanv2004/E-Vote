import os
import json
import datetime
import pandas as pd

from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path, app_data, file_data, default_election_setting_data


# folders creations
def start_folder():
    if not os.path.exists(path + r'\assets\s\abxyzc'):
        os.makedirs(path + file_path['admin_file'])
        os.makedirs(path + file_path['candidate_data'])
        dictionary = {
            "name": "E-Vote",
            "version": "0.06",
            "data": None
        }

        with open(path + r'\assets\s\abxyzc', "w") as outfile:
            json.dump(dictionary, outfile)


# file creations
def app_start(app_start_data_list1: list):
    app_start_data_dict1: dict = {"topic": [
        "app_version",
        "institution_type",
        "institution_name",
        "logo",
        "theme",
        "server",
        "server_type",
        "installation_date",
        "installation_time",
        "update_date"
    ],
        "values": [
            app_data['version'],
            app_start_data_list1[0],
            app_start_data_list1[1],
            None,
            "system",
            None,
            None,
            datetime.date.today(),
            datetime.datetime.now().strftime("%H:%M:%S"),
            None
        ]
    }

    app_data_sys_df = pd.DataFrame(app_start_data_dict1)
    election_df = pd.DataFrame(columns=['name', 'path'])
    admin_data_df = pd.DataFrame(columns=["id", "name", "mail_id", "password", "permission", "theme", "image"])
    admin_login = pd.DataFrame(columns=["id", "date", "time"])

    app_data_sys_df.to_json(path + file_path['app_data'], orient='table', index=False)
    election_df.to_csv(path + file_path['election_data'], index=False)
    admin_data_df.to_json(path + file_path['admin_data'], orient='table', index=False)
    admin_login.to_json(path + file_path['admin_login_data'], orient='table', index=False)


def new_election_creation_folder(tittle: str):
    election_path = path + file_path['candidate_data'] + rf'\{tittle}'
    os.makedirs(election_path)
    os.makedirs(election_path + r'\images')
    os.makedirs(election_path + rf'\{file_data["vote_data"]}')
    ser1 = pd.Series(default_election_setting_data)
    ser1.loc["election-name"] = tittle
    ser1.loc["created-date"] = date.today()
    ser1.loc["created-time"] = datetime.now().strftime("%H:%M:%S")
    ser1.to_json(election_path + fr"\{file_data['election_settings']}", orient='table', index=True)

    category_df = pd.DataFrame(columns=["id", "category", 'qualification'])
    candidate_df = pd.DataFrame(
        columns=['id', 'candidate_name', 'category', 'verification', 'qualification', 'image', 'date-time',
                 'created_by']
    )
    candidate_df.to_json(election_path + rf'\{file_data["candidate_data"]}', index=False, orient='table')
    category_df.to_csv(election_path + rf'\{file_data["category_data"]}', index=False)
