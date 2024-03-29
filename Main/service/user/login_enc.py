import pandas as pd
from secrets import compare_digest

from ..enc.encryption import decrypter
from ..files.write_files import login_details_update
from ..scr.check_installation import path
from ..scr.loc_file_scr import file_path

teme_data = None


def login_checker(entry1: str, entry2: str):
    global teme_data
    val_ = False

    staff_df = pd.read_json(path + file_path["admin_data"], orient='table')

    for i in range(len(staff_df)):
        if compare_digest(decrypter(staff_df.loc[i].values[1]), entry1):
            if compare_digest(decrypter(staff_df.loc[i].values[3]), entry2):
                teme_data = [staff_df.loc[i].values[0],
                             decrypter(staff_df.loc[i].values[1]),
                             staff_df.loc[i].values[4],
                             staff_df.loc[i].values[5]
                             ]
                val_ = True
                login_details_update(i)
                break

    return val_
