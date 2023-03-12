import re
from time import sleep
import flet as ft
import pandas as pd

from Main.authentication.encrypter.encryption import decrypter
from Main.authentication.files.write_files import admin_data_in
from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path

user_name, mail_id, password = False, False, False


def staff_add_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Staff > Add Staff"

    # Functions
    def back_staff_add_page(e):
        from Main.pages.staff_home import staff_home_page
        if len(name_entry.value) != 0:
            unsaved_dialogs(page, content_column, title_text)
        elif len(mail_id_entry.value) != 0:
            unsaved_dialogs(page, content_column, title_text)
        elif len(password_entry.value) != 0:
            unsaved_dialogs(page, content_column, title_text)
        else:
            content_column.clean()
            content_column.update()
            staff_home_page(page, content_column, title_text)

    ad_df = pd.read_json(path + file_path['admin_data'], orient='table')
    check_list: list = []
    for i in range(len(ad_df.index)):
        check_list.append(decrypter(ad_df.loc[i].values[1]))

    def username_checker(e):
        global user_name
        if len(name_entry.value) != 0:
            save_button.disabled = False
        else:
            save_button.disabled = True
        save_button.update()
        if len(name_entry.value) != 0:
            if name_entry.value in check_list:
                name_entry.error_text = "This Username is already taken!"
                name_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
                user_name = False
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
        mail_id_entry.on_change = mail_id_checker
        if len(mail_id_entry.value) != 0:
            if re.fullmatch(mail_check, mail_id_entry.value):
                mail_id_entry.suffix_icon = ft.icons.CHECK_CIRCLE
                mail_id_entry.error_text = None
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
        password_entry.on_change = password_checker
        if len(password_entry.value) != 0:
            if len(password_entry.value) >= 8:
                password = True
                password_entry.error_text = None
            else:
                password_entry.error_text = "Password should be least 8 characters long!"
                password = False
        else:
            password = False
            password_entry.error_text = "Enter the Password"
            password_entry.on_change = password_checker
        password_entry.update()

    def on_click_save(e):
        username_checker(e)
        mail_id_checker(e)
        password_checker(e)

        if user_name is True:
            if mail_id is True:
                if password is True:
                    if permission_dropdown.value == 'Yes':
                        permission_y_dialogs(page, content_column, [name_entry.value,
                                                                    mail_id_entry.value,
                                                                    password_entry.value], title_text)
                    else:
                        save(page, content_column, [name_entry.value, mail_id_entry.value,
                                                    password_entry.value, False], title_text)
                else:
                    password_entry.focus()
                    password_entry.update()
            else:
                mail_id_entry.focus()
                mail_id_entry.update()
        else:
            name_entry.focus()
            name_entry.update()

    # Main Text
    main_staff_add_text = ft.Text(
        value="Add Staff",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    # Button
    back_staff_home_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip="Back",
        on_click=back_staff_add_page,
    )

    question_button = ft.PopupMenuButton(
        icon=ft.icons.QUESTION_ANSWER_ROUNDED,
        tooltip="Questions?",
        items=[
            ft.PopupMenuItem(
                icon=ft.icons.ADMIN_PANEL_SETTINGS_ROUNDED,
                text="What is Admin Permission?",
                # on_click=
            ),
        ]
    )

    save_button = ft.ElevatedButton(
        text="Save",
        height=50,
        width=150,
        disabled=True,
        on_click=on_click_save,
    )

    # Input Field
    name_entry = ft.TextField(
        hint_text="Enter the Username",
        width=450,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        prefix_icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
        on_submit=on_click_save,
        on_change=username_checker,
    )

    mail_id_entry = ft.TextField(
        hint_text="Enter the Mail id",
        width=450,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        prefix_icon=ft.icons.MAIL,
        border_color=ft.colors.SECONDARY,
        on_submit=on_click_save,
    )

    password_entry = ft.TextField(
        hint_text="Enter the Password",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.icons.PASSWORD_ROUNDED,
        width=450,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        border_color=ft.colors.SECONDARY,
        on_submit=on_click_save,
    )

    permission_dropdown = ft.Dropdown(
        hint_text="Choose Admin permission",
        width=450,
        helper_text="Default value No",
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        options=[
            ft.dropdown.Option("Yes"),
            ft.dropdown.Option("No"),
        ],
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        border_color=ft.colors.SECONDARY,
    )

    add_staff_column_data = ft.Column(
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
        width=450,
        spacing=30,
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
                ft.Row(
                    [
                        question_button,
                    ],
                    alignment=ft.MainAxisAlignment.END,
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
                add_staff_column_data,
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


def unsaved_dialogs(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    def on_close(e):
        alertdialog.open = False
        page.update()

    def discard(e):
        from Main.pages.staff_home import staff_home_page
        alertdialog.open = False
        page.update()
        content_column.clean()
        content_column.update()
        staff_home_page(page, content_column, title_text)

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Discard?"
        ),
        content=ft.Text(
            value="Your changes have not been saved",
        ),
        actions=[
            ft.TextButton(
                text="Discard",
                on_click=discard,
            ),
            ft.TextButton(
                text="Save",
                on_click=on_close,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()


def permission_y_dialogs(page: ft.Page, content_column: ft.Column, list1: list, title_text: ft.Text):
    def on_close(e):
        alertdialog.open = False
        page.update()

    def save_data(e):
        list1.append(True)
        alertdialog.open = False
        page.update()
        save(page, content_column, list1, title_text)

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
                    # on_click=
                )
            ],
            height=40,
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


def save(page: ft.Page, content_column: ft.Column, list1: list, title_text: ft.Text):
    page.splash = ft.ProgressBar()
    page.update()
    from Main.functions.snack_bar import snack_bar1
    from Main.pages.staff_home import staff_home_page
    from Main.functions.dialogs import loading_dialogs
    sleep(0.2)
    loading_dialogs(page, "Saving...", 2)
    admin_data_in([list1[0], list1[1], list1[2], list1[3]])
    page.splash = None
    page.update()
    content_column.clean()
    content_column.update()
    staff_home_page(page, content_column, title_text)
    snack_bar1(page, "Successfully Added")
