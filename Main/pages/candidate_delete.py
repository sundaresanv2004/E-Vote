from time import sleep
import flet as ft
import pandas as pd


def delete_candidate_dialogs(page: ft.Page, index_df, view):
    def del_ok(e):
        page.snack_bar = ft.ProgressBar()
        page.update()
        from ..functions.snack_bar import snack_bar1
        from .candidate_home import display_candidate
        from ..service.files.write_files import delete_candidate
        from ..functions.dialogs import loading_dialogs
        from Main.service.scr.loc_file_scr import file_data
        import Main.service.scr.election_scr as ee
        delete_candidate(index_df)
        alertdialog.open = False
        page.update()
        sleep(0.2)
        loading_dialogs(page, "Deleting...", 0.5)
        sleep(0.1)
        page.snack_bar = False
        snack_bar1(page, "Successfully Deleted.")
        page.update()
        display_candidate(page)
        candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')
        list1 = candidate_data_df.index.values
        if view is True:
            from .candidate_profile import candidate_profile_page
            if index_df in list1:
                candidate_profile_page(page, index_df)
            elif index_df - 1 in list1:
                candidate_profile_page(page, index_df - 1)

    def on_close(e):
        alertdialog.open = False
        page.update()
        if view is True:
            sleep(0.1)
            from .candidate_profile import candidate_profile_page
            candidate_profile_page(page, index_df)

    # AlertDialog
    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Delete this record?",
            font_family='Verdana',
        ),
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


"""
def approve_dialogs(page: ft.Page, content_column: ft.Column, title_text, id_val, ver_val, page_type):
    from .candidate_profile import candidate_profile_page

    def on_no(e):
        alertdialog.open = False
        page.update()
        if page_type:
            sleep(0.1)
            candidate_profile_page(page, content_column, title_text, id_val)

    def on_yes(e):
        from ..authentication.files.write_files import change_verification
        alertdialog.open = False
        page.update()
        change_verification(page, id_val)
        if page_type:
            sleep(0.1)
            candidate_profile_page(page, content_column, title_text, id_val)
        else:
            from Main.pages.candidate_home import candidate_home_page
            page.update()
            content_column.clean()
            content_column.update()
            candidate_home_page(page, content_column, title_text)

    if ver_val == False:
        ver_text_1 = ft.Text(
            value="Would you like to approve this candidate for the position?"
        )
    else:
        ver_text_1 = ft.Text(
            value="Would you like to reject this candidate from the position?"
        )

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Make Sure",
        ),
        content=ver_text_1,
        actions=[
            ft.TextButton(
                text="Yes",
                on_click=on_yes,
            ),
            ft.TextButton(
                text="No",
                on_click=on_no,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()
"""
