import flet as ft
import pandas as pd
import re
from time import sleep

from ..service.enc.encryption import decrypter
from ..service.scr.check_installation import path
from ..service.scr.loc_file_scr import file_path, warnings

user_name, mail_id, password = False, False, False
alertdialog1_staff = ft.AlertDialog(modal=True)
val_list_staff = ["", "", "", False]
index_val1 = None
first = False


def staff_edit_page(page: ft.Page, index_val, view):
    import Main.service.user.login_enc as cc
    global alertdialog1_staff, val_list_staff, index_val1, first
    index_val1 = index_val

    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    index_df = staff_df.loc[index_val].values[0]

    def on_close(e):
        global val_list_staff, index_val1, first
        index_val1 = None
        first = False
        val_list_staff = ["", "", "", False]
        alertdialog1_staff.open = False
        page.update()
        sleep(0.2)
        if view is True:
            from Main.pages.staff_profile import staff_profile_page
            staff_profile_page(page, index_df)

    if first is False:
        val_list_staff = [decrypter(staff_df[staff_df.id == index_df].values[0][1]),
                          decrypter(staff_df[staff_df.id == index_df].values[0][2]),
                          decrypter(staff_df[staff_df.id == index_df].values[0][3]),
                          staff_df[staff_df.id == index_df].values[0][4]]
        first = True

    check_list: list = []
    for i in range(len(staff_df.index)):
        if staff_df.loc[i].values[0] != index_df:
            check_list.append(decrypter(staff_df.loc[i].values[1]))

    def username_checker(e):
        global user_name, val_list_staff
        val_list_staff[0] = name_entry.value
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

    mail_check = r'/b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/.[A-Z|a-z]{2,}/b'

    def mail_id_checker(e):
        global mail_id, val_list_staff
        val_list_staff[1] = mail_id_entry.value
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
        global password, val_list_staff
        val_list_staff[2] = password_entry.value
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
        global val_list_staff
        username_checker(e)
        mail_id_checker(e)
        password_checker(e)
        if permission_dropdown.value == 'Yes':
            val_list_staff[3] = True
        elif permission_dropdown.value == "No":
            val_list_staff[3] = False

        if val_list_staff[0] != decrypter(staff_df[staff_df.id == index_df].values[0][1]):
            save_button.disabled = False
        elif val_list_staff[1] != decrypter(staff_df[staff_df.id == index_df].values[0][2]):
            save_button.disabled = False
        elif val_list_staff[2] != decrypter(staff_df[staff_df.id == index_df].values[0][3]):
            save_button.disabled = False
        elif val_list_staff[3] != staff_df[staff_df.id == index_df].values[0][4]:
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
                            edit_permission_y_dialogs(page, index_df, view)
                        else:
                            save(page, index_df, view)
                    else:
                        save(page, index_df, view)
                else:
                    password_entry.focus()
                    password_entry.update()
            else:
                mail_id_entry.focus()
                mail_id_entry.update()
        else:
            name_entry.focus()
            name_entry.update()

    # Input Field
    name_entry = ft.TextField(
        hint_text="Enter the Username",
        width=400,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        prefix_icon=ft.icons.PERSON_ROUNDED,
        autofocus=True,
        on_submit=on_click_save,
        on_change=changes_checker,
    )

    mail_id_entry = ft.TextField(
        hint_text="Enter the Mail id",
        width=400,
        border=ft.InputBorder.OUTLINE,
        prefix_icon=ft.icons.MAIL_ROUNDED,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=on_click_save,
        on_change=changes_checker,
    )

    password_entry = ft.TextField(
        hint_text="Enter the Password",
        width=400,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border=ft.InputBorder.OUTLINE,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        border_radius=9,
        on_submit=on_click_save,
        on_change=changes_checker,
    )

    if len(val_list_staff[1]) != 0:
        mail_id_entry.value = val_list_staff[1]

    if len(val_list_staff[0]) != 0:
        name_entry.value = val_list_staff[0]

    if len(val_list_staff[2]) != 0:
        password_entry.value = val_list_staff[2]

    permission_dropdown = ft.Dropdown(
        hint_text="Choose Admin permission",
        text_style=ft.TextStyle(font_family='Verdana'),
        border=ft.InputBorder.OUTLINE,
        width=400,
        border_radius=9,
        color=ft.colors.BLACK,
        options=[
            ft.dropdown.Option("Yes"),
            ft.dropdown.Option("No"),
        ],
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        on_change=changes_checker,
    )

    if val_list_staff[3]:
        permission_dropdown.value = "Yes"
    else:
        permission_dropdown.value = "No"

    if cc.teme_data[2] != True or index_df == 1:
        permission_dropdown.disabled = True

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
                        spacing=41,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        width=450,
    )

    # alertdialog1_staff
    alertdialog1_staff.content = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Edit Staff",
                                weight=ft.FontWeight.BOLD,
                                size=25,
                                font_family='Verdana',
                            ),
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
        height=450,
        width=450,
    )

    save_button = ft.TextButton(
        text="Save Changes",
        disabled=True,
        on_click=on_click_save,
    )

    alertdialog1_staff.actions = [
        save_button
    ]

    alertdialog1_staff.actions_alignment = ft.MainAxisAlignment.END

    page.dialog = alertdialog1_staff
    alertdialog1_staff.open = True
    page.update()
    changes_checker('e')


def edit_permission_y_dialogs(page: ft.Page, index_val, view):
    global alertdialog1_staff, index_val1

    def on_close(e):
        alertdialog1_staff.title = None
        staff_edit_page(page, index_val1, view)

    def save_data(e):
        global val_list_staff
        alertdialog1_staff.title = None
        val_list_staff[3] = True
        alertdialog1_staff.open = False
        page.update()
        sleep(0.2)
        save(page, index_val, view)

    def on_admin_permission(e):
        alertdialog1_staff.open = False
        page.update()
        sleep(0.2)
        from ..functions.dialogs import message_dialogs
        message_dialogs(page, "Admin Permission?")

    alertdialog1_staff.title = ft.Text(
        value="Make Sure",
    )

    alertdialog1_staff.content = ft.Column(
        [
            ft.Text(
                value="Do you want to give them admin permission?",
            ),
            ft.TextButton(
                text="Learn more.",
                on_click=lambda _: y_admin_permission(page, view),
            )
        ],
        height=70,
        width=340,
    )

    alertdialog1_staff.actions = [
        ft.TextButton(
            text="Save",
            on_click=save_data,
        ),
        ft.TextButton(
            text="Change",
            on_click=on_close,
        ),
    ]

    alertdialog1_staff.actions_alignment = ft.MainAxisAlignment.END

    page.update()


def y_admin_permission(page: ft.Page, view):
    global alertdialog1_staff

    # Functions
    def on_ok(e):
        alertdialog1_staff.title = None
        staff_edit_page(page, index_val1, view)

    # alertdialog1_staff data

    alertdialog1_staff.title = ft.Text(
        font_family='Verdana',
        value="Admin Permission?",
    )

    alertdialog1_staff.content = ft.Text(
        value=f'{warnings["Admin Permission?"]}',
    )

    alertdialog1_staff.actions = [
        ft.TextButton(
            text="Ok",
            on_click=on_ok,
        ),
    ]

    alertdialog1_staff.actions_alignment = ft.MainAxisAlignment.END

    page.update()


def save(page: ft.Page, index_val, view):
    global val_list_staff, index_val1, first
    import Main.service.user.login_enc as cc
    from ..functions.snack_bar import snack_bar1
    from ..service.files.write_files import edit_staff_data
    from .staff_home import display_staff
    from ..functions.dialogs import loading_dialogs
    alertdialog1_staff.open = False
    page.update()
    edit_staff_data([val_list_staff[0], val_list_staff[1], val_list_staff[2], val_list_staff[3]], index_val)
    display_staff(page)
    snack_bar1(page, "Successfully Updated")
    index_val1 = None
    first = False
    val_list_staff = ["", "", "", False]
    if cc.teme_data[0] == index_val:
        sleep(0.3)
        if cc.teme_data[2] != val_list_staff[3]:
            page.splash = ft.ProgressBar()
            page.update()
            from .menubar import update
            update()
            from main import main
            loading_dialogs(page, "Logging out...", 3)
            sleep(0.1)
            page.splash = None
            page.update()
            page.clean()
            main(page)
    else:
        if view is True:
            from Main.pages.staff_profile import staff_profile_page
            staff_profile_page(page, index_val)
