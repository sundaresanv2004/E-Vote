from time import sleep
import flet as ft
import pandas as pd

from ..service.scr.check_installation import path
from ..service.scr.loc_file_scr import file_path
from ..functions.dialogs import loading_dialogs


def delete_staff_dialogs(page: ft.Page, index_df, view):
    # Functions
    def del_ok(e):
        from Main.pages.staff_home import display_staff
        from ..service.files.write_files import delete_staff_data
        from ..functions.snack_bar import snack_bar1
        import Main.service.user.login_enc as cc
        staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
        delete_staff_data(index_df)
        alertdialog.open = False
        page.update()
        sleep(0.2)
        loading_dialogs(page, "Deleting...", 1)
        sleep(0.1)
        snack_bar1(page, "Successfully Deleted.")
        display_staff(page)
        if cc.teme_data[0] == index_df:
            page.splash = ft.ProgressBar()
            page.update()
            from .menubar import update
            update()
            from main import main
            loading_dialogs(page, "Logging out...", 4)
            sleep(0.2)
            page.splash = None
            page.update()
            page.clean()
            main(page)
        else:
            if view is True:
                val = list(staff_df['id'].values)
                from Main.pages.staff_profile import staff_profile_page
                staff_profile_page(page, val[val.index(index_df)-1])

    def on_close(e):
        alertdialog.open = False
        page.update()
        if view is True:
            sleep(0.1)
            from Main.pages.staff_profile import staff_profile_page
            staff_profile_page(page, index_df)

    # AlertDialog
    alertdialog = ft.AlertDialog(
        title=ft.Text(
            value="Delete this record?",
            font_family='Verdana',
        ),
        modal=True,
        actions=[
            ft.TextButton(
                text="Ok",
                on_click=del_ok,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_close,
            ),
        ],
        content=ft.Text(
            value="This record will be deleted forever.",
            font_family='Verdana',
        ),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()
