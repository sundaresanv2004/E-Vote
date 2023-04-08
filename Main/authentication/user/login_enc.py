import pandas as pd

from Main.authentication.encrypter.encryption import decrypter
from Main.authentication.files.write_files import login_details_update
from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path

# admin_login_df = pd.read_json(path + file_path['admin_data'], orient='table')
# admin_data_df1 = admin_login_df.loc[0].values
teme_data = None  # [admin_data_df1[0], decrypter(admin_data_df1[1]), admin_data_df1[4], admin_data_df1[5]]


def login_checker(entry1: str, entry2: str):
    global teme_data
    val_ = False

    staff_df = pd.read_json(path + file_path["admin_data"], orient='table')

    for i in range(len(staff_df)):
        if decrypter(staff_df.loc[i].values[1]) == entry1:
            if decrypter(staff_df.loc[i].values[3]) == entry2:
                teme_data = [staff_df.loc[i].values[0],
                             decrypter(staff_df.loc[i].values[1]),
                             staff_df.loc[i].values[4],
                             staff_df.loc[i].values[5]
                             ]
                val_ = True
                login_details_update(i)
                break

    return val_
