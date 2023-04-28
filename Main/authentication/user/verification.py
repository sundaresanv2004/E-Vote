import flet as ft
import pandas as pd

import Main.authentication.scr.election_scr as ee
from ..scr.loc_file_scr import file_data, file_path


def verification_page(page: ft.Page):
    from ..files.vote_settings_write import lock_and_unlock
    from ..encrypter.encryption import decrypter

    # Functions
    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    def save_on(e):
        ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        if len(entry1.value) != 0:
            if entry1.value == decrypter(ele_ser.loc['code'].values[0]):
                entry1.error_text = None
                message_alertdialog.open = False
                page.update()
            else:
                entry1.error_text = "Invalid Code"
                entry1.focus()
                entry1.update()
        else:
            entry1.error_text = "Enter the Code"
            entry1.focus()
            entry1.update()

    entry1 = ft.TextField(
        hint_text="Enter the Code",
        border=ft.InputBorder.OUTLINE,
        width=350,
        border_radius=9,
        password=True,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        capitalization=ft.TextCapitalization.WORDS,
        on_submit=save_on,
    )

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Vote",
        ),
        content=ft.Column(
            [
                entry1
            ],
            width=350,
            height=70,
        ),
        actions=[
            ft.TextButton(
                text="Submit",
                on_click=save_on,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()
