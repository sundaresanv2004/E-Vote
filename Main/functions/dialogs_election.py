import flet as ft
import pandas as pd

import Main.authentication.scr.election_scr as ee
from ..authentication.scr.check_installation import path
from ..authentication.scr.loc_file_scr import file_data, file_path


def edit_election_name(page: ft.Page):
    # Functions
    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    election_data = pd.read_csv(path + file_path["election_data"])

    def save_on(e):
        if len(entry1.value) != 0:
            if entry1.value not in election_data['name'].values:
                entry1.error_text = None
                entry1.update()
                from ..authentication.files.settings_write import change_election_name
                change_election_name(entry1.value)
                message_alertdialog.open = False
                page.update()
            else:
                entry1.error_text = "This election name already been used"
                entry1.focus()
                entry1.update()
        else:
            entry1.error_text = "Enter the Election Name"
            entry1.focus()
            entry1.update()

    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')

    entry1 = ft.TextField(
        hint_text="Enter the Election Name",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        value=ele_ser.loc['election-name'].values[0],
        capitalization=ft.TextCapitalization.WORDS,
    )

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Change Election Name",
        ),
        content=ft.Column(
            [
                entry1,
            ],
            height=70,
            width=350,
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Save",
                on_click=save_on,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()
