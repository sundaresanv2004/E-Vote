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
                text="Save",
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


def passcode_election(page: ft.Page, switch_data: ft.Switch):
    from ..authentication.scr.loc_file_scr import messages
    from ..authentication.files.settings_write import first_lock

    # Functions
    def on_ok(e):
        switch_data.value = False
        message_alertdialog.open = False
        page.update()

    entry1 = ft.TextField(
        hint_text="Enter the Code",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        max_length=5,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        capitalization=ft.TextCapitalization.WORDS,
    )

    def save_on(e):
        if len(entry1.value) == 5:
            entry1.error_text = None
            message_alertdialog.open = False
            page.update()
            first_lock(entry1.value)
        else:
            entry1.error_text = "Enter the Code"
            entry1.focus()
            entry1.update()

    def on_next1(e):
        message_alertdialog.title = ft.Text(value="2-Step Verification")
        message_alertdialog.content = ft.Column(
            [
                entry1
            ],
            height=70,
            width=350,
        )

        message_alertdialog.actions = [
            ft.TextButton(
                text="Save",
                on_click=save_on,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ]
        page.update()

    def on_next(e):
        message_alertdialog.title = ft.Text(value="Make Sure?")
        message_alertdialog.content = ft.Column(
            [
                ft.Text(value=messages["code_text2"],
                        size=15),
            ],
            height=100,
        )

        message_alertdialog.actions = [
            ft.TextButton(
                text="Next",
                on_click=on_next1,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ]
        page.update()

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"2-Step Verification",
        ),
        content=ft.Column(
            [
                ft.Text(
                    value=messages["code_text1"],
                    size=15,
                ),
            ],
            height=100,
        ),
        actions=[
            ft.TextButton(
                text="Next",
                on_click=on_next,
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


def lock_unlock_data(page: ft.Page, switch_data: ft.Switch):
    from ..authentication.encrypter.encryption import decrypter
    from ..authentication.files.settings_write import lock_and_unlock

    # Functions
    def on_ok(e):
        if switch_data.value:
            switch_data.value = False
        else:
            switch_data.value = True
        message_alertdialog.open = False
        page.update()

    def save_on(e):
        ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        if len(entry1.value) != 0:
            if entry1.value == decrypter(ele_ser.loc['code'].values[0]):
                entry1.error_text = None
                message_alertdialog.open = False
                page.update()
                lock_and_unlock()
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
        max_length=5,
        password=True,
        can_reveal_password=True,
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
            value=f"2-Step Verification",
        ),
        content=ft.Column(
            [
                entry1
            ],
            height=70,
            width=350,
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


def category_order(page):
    from ..authentication.scr.loc_file_scr import messages

    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    def on_next1(e):
        pass

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def on_next(e):
        message_alertdialog.title = ft.Text(value="Read")
        message_alertdialog.content = ft.Text(value=messages['final_list'])
        message_alertdialog.actions = [
            ft.TextButton(
                text="Next",
                on_click=on_next1,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ]

    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    if ele_ser.loc['final_nomination'].values[0]:
        message_alertdialog.title = ft.Text(value="Make Sure?")
        message_alertdialog.content = ft.Text(value=messages['re_final_list'])
        message_alertdialog.actions = [
            ft.TextButton(
                text="Yes",
                on_click=on_next,
            ),
            ft.TextButton(
                text="No",
                on_click=on_ok,
            ),
        ]
    else:
        on_next('e')

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()
