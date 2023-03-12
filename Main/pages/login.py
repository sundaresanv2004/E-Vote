from time import sleep
import flet as ft

import Main.functions.theme as tt
from Main.functions.animations import menu_container_animation


def login_page(page: ft.Page, menu_container: ft.Container):
    # Functions
    def back(e):
        back_button.disabled = True
        menu_container.clean()
        page.update()
        from Main.pages.menu import menu_page
        menu_container_animation(menu_container)
        sleep(0.2)
        menu_page(page, menu_container)

    def check_username_input(e):
        if len(entry_name.value) != 0:
            entry_name.suffix_icon = None
            entry_name.error_text = None
        else:
            entry_name.error_text = "Enter the Username"
            entry_name.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        entry_name.update()

    def check_password_input(e):
        if len(entry_password.value) != 0:
            entry_password.error_text = ""
        else:
            entry_password.error_text = "Enter the Username"
        entry_password.update()

    def login_check_fun(e):
        login_waring_text.value = None
        login_waring_text.update()
        check_username_input(e)
        check_password_input(e)

        if len(entry_name.value) != 0:
            if len(entry_password.value) != 0:
                progressbar_column.controls = [progressbar_login]
                menu_container.disabled = True
                page.update()
                import Main.authentication.user.login_enc as cc
                val = cc.login_checker(entry_name.value, entry_password.value)
                sleep(1.5)
                if val is True:
                    from Main.pages.sidebar_options import admin_sidebar, staff_sidebar
                    page.clean()
                    if cc.teme_data[2] == True:
                        admin_sidebar(page)
                    else:
                        staff_sidebar(page)
                else:
                    progressbar_column.controls = None
                    menu_container.disabled = False
                    login_waring_text.value = "  Invalid Username or Password!  "
                    entry_password.value = None
                    entry_password.error_text = ""
                    entry_name.focus()
                    page.update()
                    val = False
            else:
                entry_password.focus()
                entry_password.update()
        else:
            entry_name.focus()
            entry_name.update()

    # text
    login_waring_text = ft.Text(
        size=20,
        color=ft.colors.ERROR,
    )

    # Input Fields
    entry_name = ft.TextField(
        hint_text="Enter the Username",
        width=400,
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        prefix_icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
        border=ft.InputBorder.OUTLINE,
        filled=False,
        border_radius=9,
        focused_border_color=ft.colors.PRIMARY,
        on_change=check_username_input,
        on_submit=login_check_fun,
    )

    entry_password = ft.TextField(
        hint_text="Enter the Password",
        width=400,
        border_radius=9,
        border_color=ft.colors.SECONDARY,
        autofocus=True,
        prefix_icon=ft.icons.PASSWORD_ROUNDED,
        border=ft.InputBorder.OUTLINE,
        filled=False,
        password=True,
        can_reveal_password=True,
        focused_border_color=ft.colors.PRIMARY,
        on_change=check_password_input,
        on_submit=login_check_fun,
    )

    def on_forgot_password(e):
        from Main.functions.dialogs import message_dialogs
        message_dialogs(page, 'Forgot Password?')

    # Buttons
    # back button
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip='Back',
        on_click=back,
    )

    button_forgot_password = ft.TextButton(
        text="Forgot Password?",
        on_click=on_forgot_password,
    )

    # login button
    login_button = ft.ElevatedButton(
        text="Login",
        height=50,
        width=150,
        on_click=login_check_fun,
    )

    # ProgressBar
    progressbar_login = ft.ProgressBar(
        width=465,
        bgcolor=ft.colors.TRANSPARENT,
    )
    progressbar_column = ft.Column(
        height=15,
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
                            ft.Text(
                                value="Log In",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
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
                [
                    login_waring_text,
                ]
            ),
            ft.Column(
                [
                    entry_name,
                    entry_password,
                ],
                spacing=40
            ),
            ft.Row(
                [
                    button_forgot_password,
                ],
                width=380,
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Column(
                height=15,
            ),
            ft.Row(
                [
                    login_button,
                ],
                width=400,
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Column(
                height=20,
            ),
        ],
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    menu_container.padding = 0.3
    menu_container.update()
