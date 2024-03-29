import os
import json
import datetime
import pandas as pd

from ..scr.check_installation import path
from ..scr.loc_file_scr import file_path, app_data, file_data, default_election_setting_data


# folders creations
def start_folder():
    if not os.path.exists(path + r'/data/s/abxyzc'):
        os.makedirs(path + file_path['admin_file'])
        os.makedirs(path + file_path['candidate_data'])
        dictionary = {
            "name": "E-Vote",
            "version": "2.01",
            "data": None,
            "enc": True
        }

        with open(path + r'/data/s/abxyzc', "w") as outfile:
            json.dump(dictionary, outfile)


# file creations
def app_start(app_start_data_list1):
    app_start_data_dict1: dict = {"topic": [
        "app_version",
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
            app_start_data_list1,
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


def new_election_creation_folder(title: str, folder_path):

    election_path = path + file_path['candidate_data'] + rf'/{folder_path}'
    os.makedirs(election_path)
    os.makedirs(election_path + r'/images')
    os.makedirs(election_path + rf'/{file_data["vote_data"]}')
    ser1 = pd.Series(default_election_setting_data)
    ser1.loc["election-name"] = title
    ser1.loc["created-date"] = f'{datetime.date.today()}'
    ser1.loc["created-time"] = datetime.datetime.now().strftime("%H:%M:%S")
    ser1.to_json(election_path + fr"/{file_data['election_settings']}", orient='table', index=True)

    category_df = pd.DataFrame(columns=["id", "category", 'qualification'])
    candidate_df = pd.DataFrame(
        columns=['id', 'candidate_name', 'category', 'verification', 'qualification', 'image', 'date-time',
                 'created_by']
    )
    candidate_df.to_json(election_path + rf'/{file_data["candidate_data"]}', index=False, orient='table')
    category_df.to_csv(election_path + rf'/{file_data["category_data"]}', index=False)
