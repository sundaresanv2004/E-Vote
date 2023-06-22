import shutil
from time import sleep
import flet as ft

import Main.service.scr.election_scr as ee
from Main.service.scr.check_installation import path
from Main.service.scr.loc_file_scr import file_data


def vote_exit(page: ft.Page):
    def on_no(e):
        exit_confirm_dialog.open = False
        page.update()

    def on_yes(e):
        exit_confirm_dialog.open = False
        page.update()
        page.clean()
        page.window_full_screen = False
        page.update()
        sleep(0.2)
        from main import main
        main(page)

    exit_confirm_dialog = ft.AlertDialog(
        modal=False,
        title=ft.Text("Confirm Exit"),
        content=ft.Text("Are you sure do you want to exit?", font_family='Verdana'),
        actions=[
            ft.TextButton(
                "Yes",
                on_click=on_yes,
            ),
            ft.TextButton(
                "No",
                on_click=on_no,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = exit_confirm_dialog
    exit_confirm_dialog.open = True
    page.update()


election_data_loc = rf'\{file_data["vote_data"]}\{file_data["election_data"]}'


def vote_done(page: ft.Page, appbar, main_column):
    def on_no(e):
        exit_confirm_dialog.open = False
        page.update()
        file_path = ee.current_election_path + election_data_loc
        file_destination = path + r'\backup\vdABCb2Y'
        shutil.copy(file_path, file_destination)
        from Main.pages.vote_home import vote_content_page
        vote_content_page(page, appbar, main_column)

    exit_confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Successfully Done"),
        content=ft.Text("Thank you for voting! Your data has been securely saved.", font_family='Verdana'),
        actions=[
            ft.TextButton(
                "Ok",
                on_click=on_no,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = exit_confirm_dialog
    exit_confirm_dialog.open = True
    page.update()
