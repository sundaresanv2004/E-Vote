from time import sleep

import flet as ft
import pandas as pd
import re

from ..authentication.encrypter.encryption import decrypter
from ..authentication.scr.check_installation import path
from ..authentication.scr.loc_file_scr import file_path

user_name, mail_id, password = False, False, False
back_page = None


def staff_edit_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text, index_df, view):
    global back_page
    back_page = view
    import Main.authentication.user.login_enc as cc

    # Main Text
    main_staff_add_text = ft.Text(
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    if view is not True:
        title_text.value = "Staff > Edit Staff"
        main_staff_add_text.value = "Edit Staff"
        index_df = staff_df.loc[index_df].values[0]
    else:
        title_text.value = "My Profile > Edit My Profile"
        main_staff_add_text.value = "Edit My Profile"

    # Functions
    def back_staff_edit_page(e):
        from .staff_home import staff_home_page
        from .profile import profile_home_page
        if name_entry.value != decrypter(staff_df[staff_df.id == index_df].values[0][1]):
            unsaved_edit_dialogs(page, content_column, title_text)
        elif mail_id_entry.value != decrypter(staff_df[staff_df.id == index_df].values[0][2]):
            unsaved_edit_dialogs(page, content_column, title_text)
        elif password_entry.value != decrypter(staff_df[staff_df.id == index_df].values[0][3]):
            unsaved_edit_dialogs(page, content_column, title_text)
        else:
            content_column.clean()
            content_column.update()
            if view is True:
                profile_home_page(page, content_column, title_text)
            else:
                staff_home_page(page, content_column, title_text)

    # Button
    back_staff_home_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip="Back",
        on_click=back_staff_edit_page,
    )

    check_list: list = []
    for i in range(len(staff_df.index)):
        if staff_df.loc[i].values[0] != index_df:
            check_list.append(decrypter(staff_df.loc[i].values[1]))

    def username_checker(e):
        global user_name
        if len(name_entry.value) != 0:
            if name_entry.value in check_list:
                user_name = False
                name_entry.error_text = "This Username is already taken!"
                name_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
            else:
                user_name = True
                name_entry.error_text = None
                name_entry.suffix_icon = ft.icons.CHECK_CIRCLE
        else:
            user_name = False
            name_entry.error_text = "Enter the Username"
            name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        name_entry.update()

    mail_check = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def mail_id_checker(e):
        global mail_id
        if len(mail_id_entry.value) != 0:
            if re.fullmatch(mail_check, mail_id_entry.value):
                mail_id_entry.error_text = None
                mail_id_entry.suffix_icon = ft.icons.CHECK_CIRCLE
                mail_id = True
            else:
                mail_id = False
                mail_id_entry.error_text = "Enter the Valid Mail id"
                mail_id_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
        else:
            mail_id = False
            mail_id_entry.error_text = "Enter the Mail id"
            mail_id_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        mail_id_entry.update()

    def password_checker(e):
        global password
        if len(password_entry.value) != 0:
            if len(password_entry.value) >= 8:
                password = True
                password_entry.error_text = None
            else:
                password_entry.error_text = "Password should be least 8 characters long!"
                password = False
        else:
            password_entry.error_text = "Enter the Password"
            password = False
        password_entry.update()

    def changes_checker(e):
        username_checker(e)
        mail_id_checker(e)
        password_checker(e)
        per_val = None
        if permission_dropdown.value == 'Yes':
            per_val = True
        elif permission_dropdown.value == "No":
            per_val = False

        if name_entry.value != decrypter(staff_df[staff_df.id == index_df].values[0][1]):
            save_button.disabled = False
        elif mail_id_entry.value != decrypter(staff_df[staff_df.id == index_df].values[0][2]):
            save_button.disabled = False
        elif password_entry.value != decrypter(staff_df[staff_df.id == index_df].values[0][3]):
            save_button.disabled = False
        elif per_val != staff_df[staff_df.id == index_df].values[0][4]:
            save_button.disabled = False
        else:
            save_button.disabled = True
        save_button.update()

    def on_click_save(e):
        if user_name is True:
            if mail_id is True:
                if password is True:
                    if permission_dropdown.value == 'Yes':
                        if staff_df[staff_df.id == index_df].values[0][4] != True:
                            edit_permission_y_dialogs(page, content_column, title_text, [name_entry.value,
                                                                                         mail_id_entry.value,
                                                                                         password_entry.value],
                                                      index_df)
                        else:
                            edit_ask_staff_dialogs(page, content_column, title_text, [name_entry.value,
                                                                                      mail_id_entry.value,
                                                                                      password_entry.value, True],
                                                   index_df)
                    else:
                        edit_ask_staff_dialogs(page, content_column, title_text, [name_entry.value, mail_id_entry.value,
                                                                                  password_entry.value, False],
                                               index_df)
                else:
                    password_entry.focus()
                    password_entry.update()
            else:
                mail_id_entry.focus()
                mail_id_entry.update()
        else:
            name_entry.focus()
            name_entry.update()

    name_entry = ft.TextField(
        hint_text="Enter the Username",
        width=450,
        value=decrypter(staff_df[staff_df.id == index_df].values[0][1]),
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        prefix_icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
        on_change=changes_checker,
    )

    mail_id_entry = ft.TextField(
        hint_text="Enter the Mail id",
        width=450,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        value=decrypter(staff_df[staff_df.id == index_df].values[0][2]),
        prefix_icon=ft.icons.MAIL,
        border_color=ft.colors.SECONDARY,
        on_change=changes_checker,
    )

    password_entry = ft.TextField(
        hint_text="Enter the Password",
        password=True,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        can_reveal_password=True,
        value=decrypter(staff_df[staff_df.id == index_df].values[0][3]),
        prefix_icon=ft.icons.PASSWORD_ROUNDED,
        width=450,
        border_color=ft.colors.SECONDARY,
        on_change=changes_checker,
    )

    permission_dropdown = ft.Dropdown(
        hint_text="Choose Admin permission",
        width=450,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        options=[
            ft.dropdown.Option("Yes"),
            ft.dropdown.Option("No"),
        ],
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        border_color=ft.colors.SECONDARY,
        on_change=changes_checker,
    )

    if staff_df[staff_df.id == index_df].values[0][4] is True:
        permission_dropdown.value = "Yes"
    else:
        permission_dropdown.value = "No"

    if cc.teme_data[2] != True or index_df == 1:
        permission_dropdown.disabled = True

    save_button = ft.ElevatedButton(
        height=50,
        width=150,
        text="Save Changes",
        disabled=True,
        on_click=on_click_save,
    )

    edit_staff_column_data = ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            name_entry,
                            mail_id_entry,
                            password_entry,
                            permission_dropdown,
                        ],
                        spacing=40,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    save_button,
                ],
                width=450,
                alignment=ft.MainAxisAlignment.END,
            )
        ],
        spacing=30,
        width=450,
    )

    content_column.controls = [
        ft.Row(
            [
                ft.Row(
                    [
                        back_staff_home_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        main_staff_add_text,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        ),
        ft.Divider(
            thickness=3,
            height=5,
        ),
        ft.Column(
            [
                ft.Row(
                    height=40,
                ),
                edit_staff_column_data,
                ft.Row(
                    height=10,
                )
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]

    page.update()
    changes_checker(None)


def unsaved_edit_dialogs(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    def on_close(e):
        alertdialog.open = False
        page.update()

    def discard(e):
        from .staff_home import staff_home_page
        from .profile import profile_home_page
        alertdialog.open = False
        page.update()
        content_column.clean()
        content_column.update()
        if back_page is True:
            profile_home_page(page, content_column, title_text)
        else:
            staff_home_page(page, content_column, title_text)

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Discard changes?",
        ),
        content=ft.Text(
            value="Your changes not been saved",
        ),
        actions=[
            ft.TextButton(
                text="Discard",
                on_click=discard,
            ),
            ft.TextButton(
                text="Keep editing",
                on_click=on_close,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()


def edit_ask_staff_dialogs(page: ft.Page, content_column: ft.Column, title_text: ft.Text, list1: list, index_val):
    def on_close(e):
        alertdialog.open = False
        page.update()

    def save_changes(e):
        alertdialog.open = False
        page.update()
        save(page, content_column, title_text, list1, index_val)

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Save your changes?",
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_close,
            ),
            ft.TextButton(
                text="Ok",
                on_click=save_changes,
            ),
        ],
        content=ft.Text(
            value="This record will be updated.",
        ),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()


def edit_permission_y_dialogs(page: ft.Page, content_column: ft.Column, title_text: ft.Text, list1: list, index_val):
    def on_close(e):
        alertdialog.open = False
        page.update()

    def save_data(e):
        list1.append(True)
        alertdialog.open = False
        page.update()
        sleep(0.2)
        edit_ask_staff_dialogs(page, content_column, title_text, list1, index_val)

    def on_admin_permission(e):
        alertdialog.open = False
        page.update()
        sleep(0.2)
        from ..functions.dialogs import message_dialogs
        message_dialogs(page, "Admin Permission?")

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Make Sure",
        ),
        content=ft.Column(
            [
                ft.Text(
                    value="Do you want to give them admin permission?",
                ),
                ft.TextButton(
                    text="Learn more.",
                    on_click=on_admin_permission,
                )
            ],
            height=70,
            width=340,
        ),
        actions=[
            ft.TextButton(
                text="Change",
                on_click=on_close,
            ),
            ft.TextButton(
                text="Save",
                on_click=save_data,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()


def save(page: ft.Page, content_column: ft.Column, title_text: ft.Text, list1: list, index_val):
    import Main.authentication.user.login_enc as cc
    from ..functions.snack_bar import snack_bar1
    from ..authentication.files.write_files import edit_staff_data
    from .staff_home import staff_home_page
    from ..functions.dialogs import loading_dialogs
    from .profile import profile_home_page
    from .sidebar_options import update_text

    sleep(0.1)
    loading_dialogs(page, "Saving Changes...", 1)
    edit_staff_data([list1[0], list1[1], list1[2], list1[3]], index_val)
    page.splash = None
    page.update()
    content_column.clean()
    content_column.update()
    if back_page is True:
        profile_home_page(page, content_column, title_text)
    else:
        staff_home_page(page, content_column, title_text)
    update_text(page)
    snack_bar1(page, "Successfully Updated")
    sleep(0.3)
    if cc.teme_data[0] == index_val:
        if cc.teme_data[2] != list1[3]:
            page.splash = ft.ProgressBar()
            page.update()
            from main import main
            loading_dialogs(page, "Logging out...", 4)
            sleep(0.1)
            page.splash = None
            page.update()
            page.clean()
            main(page)
