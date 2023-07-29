import flet as ft
import pandas as pd
import re

from ..service.enc.encryption import decrypter
from ..service.files.write_files import admin_data_in
from ..service.scr.check_installation import path
from ..service.scr.loc_file_scr import file_path
from ..service.scr.loc_file_scr import warnings

user_name, mail_id, password = False, False, False
alertdialog = ft.AlertDialog(modal=True)
val_list_staff = ["", "", "", False]


def staff_add_page(page: ft.Page):
    global alertdialog, val_list_staff

    def on_close(e):
        global val_list_staff
        val_list_staff = ["", "", "", False]
        alertdialog.open = False
        page.update()

    def username_checker(e):
        global user_name, val_list_staff
        val_list_staff[0] = name_entry.value
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
        global mail_id, val_list_staff
        val_list_staff[1] = mail_id_entry.value
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
        global password, val_list_staff
        val_list_staff[2] = password_entry.value
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
        global val_list_staff
        username_checker(e)
        mail_id_checker(e)
        password_checker(e)

        if user_name is True:
            if mail_id is True:
                if password is True:
                    if permission_dropdown.value == 'Yes':
                        permission_y_dialogs(page)
                    else:
                        val_list_staff[3] = False
                        alertdialog.open = False
                        page.update()
                        save(page)
                else:
                    password_entry.focus()
                    password_entry.update()
            else:
                mail_id_entry.focus()
                mail_id_entry.update()
        else:
            name_entry.focus()
            name_entry.update()

    def on_admin_permission(e):
        y_admin_permission(page)

    def dropdown_change(e):
        global val_list_staff
        if permission_dropdown.value == 'Yes':
            val_list_staff[3] = True
        else:
            val_list_staff[3] = False

    # Main Text
    main_staff_add_text = ft.Text(
        value="Add Staff",
        weight=ft.FontWeight.BOLD,
        size=25,
        font_family='Verdana',
    )

    ad_df = pd.read_json(path + file_path['admin_data'], orient='table')
    check_list: list = []
    for i in range(len(ad_df.index)):
        check_list.append(decrypter(ad_df.loc[i].values[1]))

    # Input Field
    name_entry = ft.TextField(
        hint_text="Enter the Username",
        width=400,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        autofocus=True,
        prefix_icon=ft.icons.PERSON_ROUNDED,
        on_submit=on_click_save,
        on_change=username_checker,
    )

    mail_id_entry = ft.TextField(
        hint_text="Enter the Mail id",
        width=400,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        prefix_icon=ft.icons.MAIL_ROUNDED,
        on_submit=on_click_save,
        on_change=mail_id_checker,
    )

    password_entry = ft.TextField(
        hint_text="Enter the Password",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        width=400,
        border=ft.InputBorder.OUTLINE,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        border_radius=9,
        on_submit=on_click_save,
        on_change=password_checker,
    )

    if len(val_list_staff[0]) != 0:
        name_entry.value = val_list_staff[0]

    if len(val_list_staff[1]) != 0:
        mail_id_entry.value = val_list_staff[1]

    if len(val_list_staff[2]) != 0:
        password_entry.value = val_list_staff[2]

    permission_dropdown = ft.Dropdown(
        hint_text="Choose Admin permission",
        text_style=ft.TextStyle(font_family='Verdana'),
        width=400,
        helper_text="Default value No",
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        color=ft.colors.BLACK,
        options=[
            ft.dropdown.Option("Yes"),
            ft.dropdown.Option("No"),
        ],
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        on_change=dropdown_change,
    )

    if val_list_staff[3]:
        permission_dropdown.value = "Yes"

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
        ],
        width=450,
    )

    # AlertDialog
    alertdialog.content = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            main_staff_add_text,
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
            add_staff_column_data,
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=480,
        width=450,
    )

    save_button = ft.TextButton(
        text="Save",
        on_click=on_click_save,
    )

    if len(val_list_staff[0]) == 0:
        save_button.disabled = True
    else:
        save_button.disabled = False

    alertdialog.actions = [
        ft.TextButton(
            text="What is Admin Permission?",
            on_click=on_admin_permission,
        ),
        save_button
    ]

    alertdialog.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()


def y_admin_permission(page: ft.Page):
    global alertdialog

    # Functions
    def on_ok(e):
        alertdialog.title = None
        staff_add_page(page)

    # AlertDialog data

    alertdialog.title = ft.Text(
        value="Admin Permission?",
        font_family='Verdana',
    )

    alertdialog.content = ft.Text(
        value=f'{warnings["Admin Permission?"]}',
    )

    alertdialog.actions = [
        ft.TextButton(
            text="Ok",
            on_click=on_ok,
        ),
    ]

    alertdialog.actions_alignment = ft.MainAxisAlignment.END

    page.update()


def permission_y_dialogs(page: ft.Page):
    global alertdialog

    def on_close(e):
        alertdialog.title = None
        staff_add_page(page)

    def save_data(e):
        global val_list_staff, alertdialog
        val_list_staff[3] = True
        alertdialog.title = None
        alertdialog.open = False
        page.update()
        save(page)

    def on_admin_permission(e):
        y_admin_permission(page)

    alertdialog.title = ft.Text(
        value="Make Sure",
        font_family='Verdana',
    )

    alertdialog.content = ft.Column(
        [
            ft.Text(
                value="Do you want to give them admin permission?",
                font_family='Verdana',
            ),
            ft.TextButton(
                text="Learn more.",
                on_click=on_admin_permission
            )
        ],
        height=70,
        width=340,
    )

    alertdialog.actions = [
        ft.TextButton(
            text="Save",
            on_click=save_data,
        ),
        ft.TextButton(
            text="Change",
            on_click=on_close,
        ),
    ]
    alertdialog.actions_alignment = ft.MainAxisAlignment.END

    page.update()


def save(page: ft.Page):
    global val_list_staff, alertdialog
    page.splash = ft.ProgressBar()
    page.update()
    from ..functions.snack_bar import snack_bar1
    from .staff_home import display_staff
    admin_data_in([val_list_staff[0], val_list_staff[1], val_list_staff[2], val_list_staff[3]])
    page.splash = None
    page.update()
    val_list_staff = ["", "", "", False]
    display_staff(page)
    snack_bar1(page, "Successfully Added")
