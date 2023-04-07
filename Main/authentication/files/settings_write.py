import pandas as pd

import Main.authentication.scr.election_scr as ee
from ..scr.loc_file_scr import file_data


def registration(val):
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    if val is True:
        ele_ser.loc['registration'] = True
    else:
        ele_ser.loc['registration'] = False
    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    from ...pages.election_home import from_page_check
    from_page_check()


def registration_date(from_val, to_val):
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    ele_ser.loc['registration_from'] = from_val
    ele_ser.loc['registration_to'] = to_val
    ele_ser.to_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table', index=True)
    from ...pages.election_home import from_page_check
    from_page_check()

