import shutil
from time import sleep

import Main.service.scr.election_scr as ee
from Main.functions.dialogs import loading_dialogs
from Main.service.scr.check_installation import path
from Main.service.scr.loc_file_scr import file_data

election_data_loc = rf'/{file_data["vote_data"]}/{file_data["election_data"]}'


def election_data_missing(page):
    file_destination = ee.current_election_path + election_data_loc
    file_path = path + r'/backup/vdABCb2Y'
    loading_dialogs(page, 'Troubleshooting...', 3)
    shutil.copy(file_path, file_destination)
    page.clean()
    page.window_full_screen = False
    page.update()
    sleep(0.2)
    from main import main
    main(page)
