from time import sleep
import flet as ft

from ..functions.dialogs import message_dialogs


def login_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    def on_hover_color(e):
        e.control.bgcolor = "#0369a1" if e.data == "true" else "#0ea5e9"
        e.control.update()

    def back(e):
        from .menu import menu_page
        content_image.height = 370
        content_image.update()
        sleep(0.3)
        content_column.clean()
        page.update()
        menu_page(page, content_image, content_column)

    def check_username_input(e):
        login_waring_text.value = None
        login_waring_text.update()
        if len(username_entry.value) != 0:
            username_entry.suffix_icon = None
            username_entry.error_text = None
        else:
            username_entry.error_text = "Enter the Username"
            username_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        username_entry.update()

    def check_password_input(e):
        login_waring_text.value = None
        login_waring_text.update()
        if len(password_entry.value) != 0:
            password_entry.error_text = ""
        else:
            password_entry.error_text = "Enter the Password"
        password_entry.update()

    def login_check_fun(e):
        check_username_input(e)
        check_password_input(e)

        if len(username_entry.value) != 0:
            if len(password_entry.value) != 0:
                button_container.content = ft.ProgressRing(color=ft.colors.WHITE)
                content_column.disabled = True
                button_container.opacity = 0.5
                button_container.bgcolor = '#295361'
                page.update()
                import Main.service.user.login_enc as cc
                val = cc.login_checker(username_entry.value, password_entry.value)
                sleep(1)
                if val is True:
                    from .menubar import menubar_page
                    page.clean()
                    if cc.teme_data[2] == True:
                        menubar_page(page, True)
                    else:
                        menubar_page(page, False)
                else:
                    button_container.content = ft.Text(
                        value="Sign Up",
                        size=20,
                        font_family='Verdana',
                        weight=ft.FontWeight.W_400,
                        color=ft.colors.WHITE,
                    )
                    content_column.disabled = False
                    button_container.opacity = 1
                    button_container.bgcolor = '#0ea5e9'
                    page.update()
                    login_waring_text.value = "  Invalid Username or Password!  "
                    password_entry.error_text = ""
                    username_entry.focus()
                    page.update()
                    val = False
            else:
                password_entry.focus()
                password_entry.update()
        else:
            username_entry.focus()
            username_entry.update()

    # text
    login_waring_text = ft.Text(
        size=20,
        color=ft.colors.ERROR,
    )

    button_container = ft.Container(
        height=50,
        width=330,
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
        on_click=login_check_fun,
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
        on_change=check_username_input,
        on_submit=login_check_fun,
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
        on_change=check_password_input,
        on_submit=login_check_fun,
    )

    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Sign In",
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
                        password_entry,
                        button_container,
                    ],
                    width=450,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
                ft.Row(
                    [
                        login_waring_text
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            width=450,
            height=320,
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=15,
        ),
        ft.Container(
            content=ft.Row(
                [
                    ft.TextButton(
                        text="Back",
                        icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        on_click=back,
                    ),
                    ft.TextButton(
                        text="Forgot Password?",
                        on_click=lambda e: message_dialogs(page, 'Forgot Password?'),
                    ),
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
