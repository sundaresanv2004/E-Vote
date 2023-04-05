from time import sleep

import flet as ft
import pandas as pd

from Main.authentication.encrypter.encryption import decrypter
from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path
import Main.authentication.user.login_enc as cc

index_val = None


def staff_profile_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text, id_index):
    global index_val
    # files
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    staff_login_df = pd.read_json(path + file_path['admin_login_data'], orient='table')
    index_val = staff_df[staff_df.id == id_index].index.values[0]

    # Functions
    def delete_on_click(e):
        alertdialog.open = False
        page.update()
        sleep(0.1)
        from Main.functions.dialogs import message_dialogs
        from Main.pages.staff_delete import delete_staff_dialogs
        if index_val == 0:
            message_dialogs(page, "Delete this record?")
        else:
            delete_staff_dialogs(page, content_column, staff_df.loc[index_val].values[0], title_text, True)

    def edit_on_click(e):
        alertdialog.open = False
        page.update()
        sleep(0.3)
        from Main.pages.staff_edit import staff_edit_page
        from Main.functions.dialogs import message_dialogs
        if index_val == 0:
            if cc.teme_data[0] == 1:
                content_column.clean()
                content_column.update()
                staff_edit_page(page, content_column, title_text, index_val, False)
            else:
                message_dialogs(page, "Edit this record?")
        else:
            content_column.clean()
            content_column.update()
            staff_edit_page(page, content_column, title_text, index_val, False)

    def on_close(e):
        alertdialog.open = False
        page.update()

    def button_check():
        if index_val == 0:
            back_button.disabled = True
        else:
            back_button.disabled = False

        if index_val == staff_df.index.max():
            next_button.disabled = True
        else:
            next_button.disabled = False

    def next_fun(e):
        global index_val
        index_val += 1
        content_change()
        page.update()

    def back_fun(e):
        global index_val
        index_val -= 1
        content_change()
        page.update()

    # Buttons
    next_button = ft.IconButton(
        icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
        icon_size=30,
        tooltip='Next',
        on_click=next_fun,
    )

    back_button = ft.IconButton(
        icon=ft.icons.KEYBOARD_ARROW_LEFT_ROUNDED,
        icon_size=30,
        tooltip="Previous",
        on_click=back_fun,
    )

    # Texts
    title1 = ft.Text(
        weight=ft.FontWeight.BOLD,
        size=25,
    )

    name_text = ft.Text(
        size=25,
    )

    mail_id_text = ft.Text(
        size=25,
    )

    password_text = ft.Text(
        size=25,
    )

    permission_icon = ft.Icon(
        size=30,
    )

    last_login_text = ft.Text(
        size=25,
    )

    def content_change():
        user_data = staff_df.loc[index_val].values
        button_check()
        title1.value = f"Staff ID: {user_data[0]}"
        name_text.value = f"Name: {decrypter(user_data[1])}"
        mail_id_text.value = f"Mail ID: {decrypter(user_data[2])}"
        if cc.teme_data[0] != 1:
            if index_val == 0:
                password_text.value = 'Password: ' + f'*' * len(decrypter(user_data[3]))
            else:
                password_text.value = f'Password: {decrypter(user_data[3])}'
        else:
            password_text.value = f'Password: {decrypter(user_data[3])}'
        if user_data[4] == True:
            permission_icon.color = ft.colors.GREEN_700
            permission_icon.name = ft.icons.DONE_ALL_ROUNDED
        else:
            permission_icon.name = ft.icons.CLOSE_ROUNDED
            permission_icon.color = ft.colors.RED_700
        if staff_login_df.loc[index_val].values[1] == False:
            last_login_text.value = "Last Login: No Data"
        else:
            date_1 = ''
            read_val = str(staff_login_df.loc[index_val].values[1])
            for i in range(10):
                date_1 += read_val[i]
            last_login_text.value = f"Last Login: {date_1} - {str(staff_login_df.loc[index_val].values[2])}"

    content_change()

    # AlertDialog
    alertdialog = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                title1,
                            ],
                            expand=True,
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
                    ]
                ),
                ft.Row(
                    [
                        back_button,
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        name_text,
                                        mail_id_text,
                                        password_text,
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    value="Permission: ",
                                                    size=25,
                                                ),
                                                permission_icon,
                                            ]
                                        ),
                                        last_login_text,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=20,
                            width=490,
                            scroll=ft.ScrollMode.ADAPTIVE,
                        ),
                        next_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    width=600,
                    height=300,
                ),
            ],
            height=350,
            width=600,
        ),
        actions=[
            ft.TextButton(
                text="Edit",
                icon=ft.icons.EDIT_ROUNDED,
                tooltip="Edit",
                on_click=edit_on_click,
            ),
            ft.TextButton(
                text="Delete",
                icon=ft.icons.DELETE_ROUNDED,
                tooltip='Delete',
                on_click=delete_on_click,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()
