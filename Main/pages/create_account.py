import re
from time import sleep
import flet as ft

from Main.functions.date_time import present_year
from Main.functions.dialogs import message_dialogs

institution_name = None


def create_account_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    global institution_name

    def back(e):
        global institution_name
        institution_name = None
        from .menu import menu_page
        content_image.height = 370
        content_image.update()
        sleep(0.2)
        content_column.clean()
        page.update()
        menu_page(page, content_image, content_column)

    def check_entry_valid(e):
        if len(type_name_entry.value) != 0:
            type_name_entry.suffix_icon = None
            type_name_entry.error_text = None
        else:
            type_name_entry.error_text = "Enter the institution name"
            type_name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        type_name_entry.update()

    def next_button_click(e):
        global institution_name
        check_entry_valid(e)

        if len(type_name_entry.value) != 0:
            button_container.content = ft.ProgressRing(color=ft.colors.WHITE)
            page.update()
            type_name_entry.disabled = True
            button_container.disabled = True
            button_container.opacity = 0.5
            button_container.bgcolor = '#295361'
            page.update()
            sleep(0.4)
            institution_name = type_name_entry.value
            content_image.height = 0
            content_image.update()
            content_column.clean()
            page.update()
            sign_up_page(page, content_image, content_column)
        else:
            type_name_entry.focus()
            page.update()

    type_name_entry = ft.TextField(
        hint_text="Enter the institution name",
        width=330,
        capitalization=ft.TextCapitalization.CHARACTERS,
        filled=False,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_entry_valid,
        on_submit=next_button_click,
    )

    if institution_name is not None:
        type_name_entry.value = institution_name

    def on_hover_color(e):
        e.control.bgcolor = "#0369a1" if e.data == "true" else "#0ea5e9"
        e.control.update()

    button_container = ft.Container(
        width=330,
        height=50,
        border_radius=10,
        bgcolor="#0ea5e9",
        on_hover=on_hover_color,
        content=ft.Text(
            value="Next",
            size=20,
            font_family='Verdana',
            weight=ft.FontWeight.W_400,
            color=ft.colors.WHITE,
        ),
        alignment=ft.alignment.center,
        animate=ft.animation.Animation(100, ft.AnimationCurve.DECELERATE),
        on_click=next_button_click,
    )

    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Create Account",
                            size=30,
                            font_family='Verdana',
                            color='#0c4a6e',
                            weight=ft.FontWeight.W_800,
                        ),
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        type_name_entry,
                        button_container,
                    ],
                    width=450,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
            ],
            width=450,
            height=240,
            spacing=20,
        ),
        ft.Container(
            ft.Row(
                [
                    ft.TextButton(
                        text="Back",
                        icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        on_click=back,
                    )
                ],
                width=450,
            ),
            bgcolor="#44CCCCCC",
            blur=ft.Blur(50, 50, ft.BlurTileMode.MIRROR),
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
        )
    ]

    page.update()


def sign_up_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    def back(e):
        content_image.height = 250
        content_image.update()
        sleep(0.4)
        content_column.clean()
        page.update()
        create_account_page(page, content_image, content_column)

    def check_username_entry(e):
        if len(username_entry.value) != 0:
            username_entry.suffix_icon = None
            username_entry.error_text = None
        else:
            username_entry.error_text = "Enter the Username"
            username_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        username_entry.update()

    # Valid Mail checker
    mail_check = r'/b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+/.[A-Z|a-z]{2,}/b'

    def check_mail_id_entry(e):
        if len(mail_id_entry.value) != 0:
            if re.fullmatch(mail_check, mail_id_entry.value):
                mail_id_entry.suffix_icon = ft.icons.CHECK_CIRCLE
                mail_id_entry.error_text = None
            else:
                mail_id_entry.error_text = "Enter the Valid Mail id"
                mail_id_entry.suffix_icon = ft.icons.CLOSE_ROUNDED
        else:
            mail_id_entry.error_text = "Enter the Mail id"
            mail_id_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        mail_id_entry.update()

    def check_password_entry(e):
        if len(password_entry.value) != 0:
            if len(password_entry.value) >= 8:
                password_entry.error_text = None
            else:
                password_entry.error_text = "Password should be least 8 characters long!"
        else:
            password_entry.error_text = "Enter the Password"
        password_entry.update()

    def on_submit_click(e):
        check_username_entry(e)
        check_mail_id_entry(e)
        check_password_entry(e)

        if len(username_entry.value) != 0:
            if len(mail_id_entry.value) != 0:
                if re.fullmatch(mail_check, mail_id_entry.value):
                    if len(password_entry.value) != 0:
                        if len(password_entry.value) >= 8:
                            button_container.content = ft.ProgressRing(color=ft.colors.WHITE)
                            page.update()
                            back_button.disabled = True
                            button_y_admin_details.disabled = True
                            username_entry.disabled = True
                            password_entry.disabled = True
                            mail_id_entry.disabled = True
                            button_container.disabled = True
                            button_container.opacity = 0.5
                            button_container.bgcolor = '#295361'
                            page.update()
                            sleep(0.5)
                            from Main.service.files.files_cre import start_folder
                            start_folder()
                            sleep(0.5)
                            from Main.service.files.files_cre import app_start
                            app_start(institution_name)
                            sleep(1)
                            from Main.service.files.write_files import admin_data_in
                            admin_data_in([username_entry.value, mail_id_entry.value, password_entry.value, True])
                            from Main.service.files.write_files import new_election_creation
                            new_election_creation(f"{present_year}-Election")
                            from ..functions.snack_bar import snack_bar1
                            sleep(1)
                            content_column.clean()
                            page.update()
                            from .all_done import all_done_page
                            all_done_page(page, content_column)
                            sleep(0.2)
                            snack_bar1(page, "All Done")
                        else:
                            password_entry.focus()
                            password_entry.update()
                    else:
                        password_entry.focus()
                        password_entry.update()
                else:
                    mail_id_entry.focus()
                    mail_id_entry.update()
            else:
                mail_id_entry.focus()
                mail_id_entry.update()
        else:
            username_entry.focus()
            username_entry.update()

    # button
    back_button = ft.TextButton(
        text="Back",
        icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
        on_click=back,
    )

    # Why admin details button
    button_y_admin_details = ft.TextButton(
        text="Read Me!",
        on_click=lambda e: message_dialogs(page, 'Read Me!'),
    )

    # Input Fields
    username_entry = ft.TextField(
        hint_text="Enter the Username",
        width=330,
        filled=False,
        prefix_icon=ft.icons.PERSON_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_username_entry,
        on_submit=on_submit_click,
    )

    mail_id_entry = ft.TextField(
        hint_text="Enter the Mail id",
        width=330,
        filled=False,
        prefix_icon=ft.icons.MAIL_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_mail_id_entry,
        on_submit=on_submit_click,
    )

    password_entry = ft.TextField(
        hint_text="Enter the Password",
        width=330,
        filled=False,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        password=True,
        can_reveal_password=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_change=check_password_entry,
        on_submit=on_submit_click,
    )

    def on_hover_color(e):
        e.control.bgcolor = "#0369a1" if e.data == "true" else "#0ea5e9"
        e.control.update()

    button_container = ft.Container(
        width=330,
        height=50,
        border_radius=10,
        bgcolor="#0ea5e9",
        on_hover=on_hover_color,
        content=ft.Text(
            value="Sign Up",
            size=20,
            font_family='Verdana',
            weight=ft.FontWeight.W_400,
            color=ft.colors.WHITE,
        ),
        alignment=ft.alignment.center,
        animate=ft.animation.Animation(100, ft.AnimationCurve.DECELERATE),
        on_click=on_submit_click,
    )

    content_column.controls = [
        ft.Row(height=20),
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Sign Up",
                            size=30,
                            font_family='Verdana',
                            color='#0c4a6e',
                            weight=ft.FontWeight.W_800,
                        ),
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        username_entry,
                        mail_id_entry,
                        password_entry,
                        button_container
                    ],
                    width=450,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=40,
                ),
            ],
            width=450,
            height=460,
            spacing=20,
            scroll=ft.ScrollMode.ADAPTIVE
        ),
        ft.Container(
            content=ft.Row(
                [
                    back_button,
                    button_y_admin_details
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                width=450,
            ),
            bgcolor='#44CCCCCC',
            blur=ft.Blur(50, 50, ft.BlurTileMode.MIRROR),
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
        )
    ]

    page.update()
