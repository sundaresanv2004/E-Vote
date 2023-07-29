from secrets import compare_digest
import pandas as pd

import Main.service.scr.election_scr as ee
from ..enc.encryption import decrypter
from ..scr.loc_file_scr import file_data


def verification_page(code):
    ele_ser = pd.read_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table')
    if compare_digest(decrypter(ele_ser.loc['code'].values[0]), code):
        return True
    else:
        return False
