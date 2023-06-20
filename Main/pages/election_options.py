from time import sleep
import flet as ft
import pandas as pd

import Main.service.scr.election_scr as ee
from ..functions.dialogs import message_dialogs
from ..service.enc.encryption import decrypter
from ..service.scr.loc_file_scr import file_data
from ..service.user.verification import verification_page


def passcode_election(page: ft.Page, switch_data: ft.Switch):
    from ..service.scr.loc_file_scr import messages
    from ..service.files.vote_settings_write import first_lock

    # Functions
    def on_ok(e):
        switch_data.value = False
        message_alertdialog.open = False
        page.update()

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
        on_submit=save_on,
        keyboard_type=ft.KeyboardType.NUMBER,
        capitalization=ft.TextCapitalization.WORDS,
    )

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
    from ..service.files.vote_settings_write import lock_and_unlock

    # Functions
    def on_ok(e):
        if switch_data.value:
            switch_data.value = False
        else:
            switch_data.value = True
        message_alertdialog.open = False
        page.update()

    def save_on(e):
        if len(entry1.value) != 0:
            if verification_page(entry1.value):
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


def category_order(page: ft.Page):
    from ..service.scr.loc_file_scr import messages
    from ..functions.order_category import order_category_option

    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    def on_next1(e):
        message_alertdialog.open = False
        page.update()
        sleep(0.1)
        order_category_option(page)

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

        page.update()

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


def forgot_code(page: ft.Page):
    from ..service.enc.code_generator import code_checker, code_generate
    import Main.service.user.login_enc as cc

    def on_close(e):
        forgot_code_dialog1.open = False
        page.update()

    def on_ok(e):
        if len(code_entry.value) != 0:
            if code_checker(code_entry.value):
                code_entry.error_text = None
                code_entry.update()
                forgot_code_dialog1.title = ft.Text("Forgot code?")
                ele_ser10 = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
                forgot_code_dialog1.content = ft.Row(
                    [
                        ft.Text(
                            value=f"Code: {decrypter(ele_ser10.loc['code'].values[0])}"
                        )
                    ]
                )
                forgot_code_dialog1.actions = [
                    ft.TextButton(
                        text="Close",
                        on_click=on_close,
                    ),
                ]
                page.update()
            else:
                code_entry.error_text = "Invalid Code!"
                code_entry.focus()
        else:
            code_entry.error_text = "Enter the code."
            code_entry.focus()
        code_entry.update()

    code_entry = ft.TextField(
        hint_text="Enter the one time code.",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        autofocus=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        capitalization=ft.TextCapitalization.WORDS,
        prefix_icon=ft.icons.PASSWORD_ROUNDED,
        on_submit=on_ok,
    )

    if cc.teme_data[0] == 1:
        code_generate(page)
        forgot_code_dialog1 = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value="2-Step verification",
                font_family='Verdana',
            ),
            content=ft.Row(
                [
                    code_entry
                ],
                width=400,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            actions=[
                ft.TextButton(
                    text="Check",
                    on_click=on_ok,
                ),
                ft.TextButton(
                    text="Cancel",
                    on_click=on_close,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = forgot_code_dialog1
        forgot_code_dialog1.open = True
        page.update()
    else:
        message_dialogs(page, "Forgot Code?")
