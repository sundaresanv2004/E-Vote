from time import sleep
import flet as ft
import pandas as pd

from ..functions.dialogs import loading_dialogs, message_dialogs
from ..functions.snack_bar import snack_bar1
import Main.service.scr.election_scr as ee
from ..service.scr.check_installation import path
from ..service.scr.loc_file_scr import file_path, file_data


def institution_name_dialogs(page: ft.Page):
    def on_ok(e):
        institution_name_dialogs1.open = False
        page.update()

    app_data_sys_df = pd.read_json(path + file_path['app_data'], orient='table')

    def check_entry_valid(e):
        if len(institution_name_entry.value) != 0:
            institution_name_entry.suffix_icon = None
            institution_name_entry.error_text = None
        else:
            institution_name_entry.error_text = "Enter the institution name"
            institution_name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        institution_name_entry.update()

    def save_name(e):
        check_entry_valid(e)
        if len(institution_name_entry.value) != 0:
            if app_data_sys_df.values[1][1] != institution_name_entry.value:
                from ..service.files.settings_write import institution_name_change
                institution_name_change(institution_name_entry.value)
                on_ok(e)
            else:
                on_ok(e)
        else:
            institution_name_entry.focus()
            institution_name_entry.update()

    institution_name_entry = ft.TextField(
        hint_text="Enter the institution name",
        width=360,
        capitalization=ft.TextCapitalization.CHARACTERS,
        filled=False,
        border_radius=9,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        value=app_data_sys_df.values[1][1],
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_entry_valid,
        on_submit=save_name,
    )

    # AlertDialog data
    institution_name_dialogs1 = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Institution Name",
            font_family='Verdana',
        ),
        content=ft.Row(
            [
                institution_name_entry
            ],
            width=400,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.TextButton(
                text="Save",
                on_click=save_name,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = institution_name_dialogs1
    institution_name_dialogs1.open = True
    page.update()


def new_election_dialogs(page: ft.Page):
    def on_ok(e):
        new_election_dialogs1.open = False
        page.update()

    election_data2 = pd.read_csv(path + file_path["election_data"])
    election_list = list(election_data2['name'])

    def check_entry_valid(e):
        if len(new_election_entry.value) != 0:
            if new_election_entry.value not in election_list:
                new_election_entry.error_text = None
                new_election_entry.suffix_icon = None
            else:
                new_election_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
                new_election_entry.error_text = "Election with this name already exists."
        else:
            new_election_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
            new_election_entry.error_text = "Enter the institution name"
        new_election_entry.update()

    def save_name(e):
        check_entry_valid(e)
        if len(new_election_entry.value) != 0:
            if new_election_entry.value not in election_list:
                new_election_dialogs1.open = False
                page.update()
                sleep(0.2)
                from ..service.files.write_files import new_election_creation
                new_election_creation(new_election_entry.value)
                loading_dialogs(page, "Creating Election...", 2)
                snack_bar1(page, "Successfully Created.")
                sleep(0.2)
                message_dialogs(page, 'Restart Required')
                page.update()
            else:
                new_election_entry.focus()
        else:
            new_election_entry.focus()
        new_election_entry.update()

    new_election_entry = ft.TextField(
        hint_text="Enter the election name",
        width=360,
        filled=False,
        border_radius=9,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_entry_valid,
        on_submit=save_name,
    )

    # AlertDialog data
    new_election_dialogs1 = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Create New Election",
            font_family='Verdana',
        ),
        content=ft.Row(
            [
                new_election_entry
            ],
            width=400,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.TextButton(
                text="Save",
                on_click=save_name,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = new_election_dialogs1
    new_election_dialogs1.open = True
    page.update()


def help_dialogs(page: ft.Page):
    from ..service.scr.loc_file_scr import all_done_message

    def on_close(e):
        help_dialogs1.open = False
        page.update()

    help_content = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                name=ft.icons.LIVE_HELP_ROUNDED,
                                size=30,
                            ),
                            ft.Text(
                                value="Help",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                font_family='Verdana',
                            ),
                        ],
                        width=450,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        key='top'
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.CLOSE_ROUNDED,
                                tooltip="Close",
                                on_click=on_close,
                            )
                        ]
                    )
                ],
                width=500,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(height=10),
            ft.Column(
                [
                    ft.Column(
                        [
                            ft.Markdown(
                                code_theme="atom-one-dark",
                                selectable=False,
                                value=all_done_message,
                                code_style=ft.TextStyle(font_family="Verdana"),
                            )
                        ],
                        width=460,
                    ),
                ],
                width=480,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(height=5),
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_CIRCLE_UP_ROUNDED,
                        tooltip='Back to top',
                        icon_size=30,
                        icon_color=ft.colors.BLACK,
                        on_click=lambda _: help_content.scroll_to(key="top", duration=1000)
                    ),
                    ft.Row(width=1)
                ],
                width=480,
                alignment=ft.MainAxisAlignment.END
            )
        ],
        width=500,
        height=570,
        scroll=ft.ScrollMode.ADAPTIVE
    )

    # AlertDialog data
    help_dialogs1 = ft.AlertDialog(
        modal=False,
        content=help_content,
    )

    # Open dialog
    page.dialog = help_dialogs1
    help_dialogs1.open = True
    page.update()


def delete_election_dialogs(page: ft.Page):
    from ..service.files.settings_write import delete_election
    from ..service.enc.code_generator import code_generate, code_checker

    def on_close(e):
        delete_election_dialogs1.open = False
        page.update()

    def on_ok(e):
        if len(code_entry.value) != 0:
            if code_checker(code_entry.value):
                code_entry.error_text = None
                code_entry.update()
                delete_election_dialogs1.open = False
                page.update()
                sleep(0.2)
                delete_election()
                loading_dialogs(page, "Deleting...", 2)
                snack_bar1(page, "Successfully Deleted.")
                sleep(0.2)
                message_dialogs(page, 'Restart Required')
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

    def del_ok(e):
        code_generate(page)
        delete_election_dialogs1.title = ft.Text(
            value="2-Step verification",
            font_family='Verdana',
        )

        delete_election_dialogs1.content = ft.Row(
            [
                code_entry
            ],
            width=400,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        delete_election_dialogs1.actions = [
            ft.TextButton(
                text="Delete",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_close,
            ),
        ]

        page.update()

    # AlertDialog
    delete_election_dialogs1 = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Delete Election?",
            font_family='Verdana',
        ),
        actions=[
            ft.TextButton(
                text="Yes",
                on_click=del_ok,
            ),
            ft.TextButton(
                text="No",
                on_click=on_close,
            ),
        ],
        content=ft.Text(
            value="Make sure!, This election will be deleted forever.",
            font_family='Verdana',
        ),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = delete_election_dialogs1
    delete_election_dialogs1.open = True
    page.update()


def election_name_dialogs(page: ft.Page):
    def on_ok(e):
        election_name_dialogs1.open = False
        page.update()

    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    election_data6 = pd.read_csv(path + file_path["election_data"])
    election_list1 = list(election_data6['name'])

    def on_election_name_change(e):
        if len(election_name_entry.value) != 0:
            if election_name_entry.value not in election_list1:
                election_name_entry.error_text = None
                election_name_entry.suffix_icon = None
            else:
                election_name_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
                election_name_entry.error_text = 'This election name already been used.'
        else:
            election_name_entry.error_text = 'Enter the election name.'
            election_name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        election_name_entry.update()

    def on_save_election_name(e):
        on_election_name_change(e)
        if len(election_name_entry.value) != 0:
            if election_name_entry.value not in election_list1:
                from ..service.files.settings_write import change_election_name
                change_election_name(election_name_entry.value)
                election_name_dialogs1.open = False
                page.update()
                snack_bar1(page, "Successfully Updated.")
            else:
                election_name_entry.focus()
        else:
            election_name_entry.focus()
        election_name_entry.update()

    election_name_entry = ft.TextField(
        hint_text="Enter the Election Name",
        width=350,
        border_radius=9,
        filled=False,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=on_save_election_name,
        on_change=on_election_name_change,
        value=ele_ser.loc['election-name'].values[0],
    )

    # AlertDialog data
    election_name_dialogs1 = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            font_family='Verdana',
            value="Institution Name",
        ),
        content=ft.Row(
            [
                election_name_entry
            ],
            width=400,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.TextButton(
                text="Save",
                on_click=on_save_election_name,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = election_name_dialogs1
    election_name_dialogs1.open = True
    page.update()


