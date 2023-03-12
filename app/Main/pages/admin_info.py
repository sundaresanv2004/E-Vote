import re
from time import sleep
import flet as ft

import Main.functions.theme as tt
from Main.functions.animations import menu_container_animation


def admin_info_page(page: ft.Page, menu_container: ft.Container, input_data1: list):
    # Functions
    def back(e):
        back_button.disabled = True
        menu_container.clean()
        page.update()
        from Main.pages.start_info import start_info_page
        sleep(0.1)
        start_info_page(page, menu_container, input_data1)

    def y_admin_details_fun(e):
        from Main.functions.dialogs import message_dialogs
        message_dialogs(page, 'Why Admin Details?')

    def check_username_entry(e):
        if len(username_entry.value) != 0:
            username_entry.suffix_icon = None
            username_entry.error_text = None
        else:
            username_entry.error_text = "Enter the Username"
            username_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        username_entry.update()

    # Valid Mail checker
    mail_check = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

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
                            progressbar_column.controls = [progressbar]
                            menu_container.disabled = True
                            page.update()
                            from Main.authentication.files.files_cre import start_folder
                            start_folder()
                            sleep(1)
                            from Main.authentication.files.files_cre import app_start
                            app_start(input_data1)
                            sleep(2)
                            from Main.authentication.files.write_files import admin_data_in
                            admin_data_in([username_entry.value, mail_id_entry.value,
                                           password_entry.value, True])
                            from Main.functions.snack_bar import snack_bar1
                            sleep(1.5)
                            menu_container.clean()
                            page.update()
                            from Main.pages.all_done import all_done_page
                            menu_container_animation(menu_container)
                            all_done_page(page, menu_container)
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

    # Main tittle
    text1 = ft.Text(
        value="Admin Details",
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    # Buttons
    # back button
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        on_click=back,
        tooltip='Back',
    )

    # next button
    submit_button = ft.ElevatedButton(
        text="Submit",
        height=50,
        width=120,
        on_click=on_submit_click,
    )

    # Why admin details button
    button_y_admin_details = ft.TextButton(
        text="Why admin Details?",
        on_click=y_admin_details_fun,
    )

    # Input Fields
    username_entry = ft.TextField(
        hint_text="Enter the Username",
        width=400,
        filled=False,
        border_radius=9,
        autofocus=True,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.SECONDARY,
        on_change=check_username_entry,
        on_submit=on_submit_click,
    )

    mail_id_entry = ft.TextField(
        hint_text="Enter the Mail id",
        width=400,
        filled=False,
        border_radius=9,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.SECONDARY,
        on_change=check_mail_id_entry,
        on_submit=on_submit_click,
    )

    password_entry = ft.TextField(
        hint_text="Enter the Password",
        width=400,
        filled=False,
        password=True,
        can_reveal_password=True,
        border_radius=9,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.SECONDARY,
        on_change=check_password_entry,
        on_submit=on_submit_click,
    )

    # Progressbar
    progressbar = ft.ProgressBar(
        bgcolor=ft.colors.TRANSPARENT,
        width=465,
    )
    progressbar_column = ft.Column(
        height=15
    )

    # alignment and data
    menu_container.content = ft.Column(
        [
            progressbar_column,
            ft.Row(
                [
                    ft.Row(
                        [
                            back_button,
                        ],
                    ),
                    ft.Row(
                        [
                            text1,
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            tt.ThemeIcon(page),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Column(
                height=10,
            ),
            ft.Column(
                [
                    username_entry,
                    mail_id_entry,
                    password_entry,
                ],
                spacing=25
            ),
            ft.Row(
                [
                    button_y_admin_details,
                ],
                width=380,
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Row(
                [
                    submit_button,
                ],
                width=400,
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Column(
                height=20,
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    menu_container.padding = 0.3
    menu_container.disabled = False
    menu_container.update()
