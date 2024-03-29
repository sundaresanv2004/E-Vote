import flet as ft

from ..service.scr.check_installation import start
from .create_account import create_account_page
import Main.service.scr.election_scr as ee
from .login import login_page
from .vote_login import vote_login_page

cont_image = None
cont_column = None


class MenuButtons(ft.UserControl):
    def __init__(self, page: ft.Page, text: str):
        super().__init__()
        self.page = page
        self.text = text
        self.cont_image = cont_image
        self.cont_column = cont_column
        self.button_container = None
        self.text_val = ft.Text(
            value=self.text,
            size=20,
            color=ft.colors.WHITE,
            font_family='Verdana',
            weight=ft.FontWeight.W_400,
        )

    def animations(self, size):
        self.cont_image.height = size
        self.cont_column.clean()
        self.page.update()

    def on_create_account(self, e):
        self.animations(250)
        create_account_page(self.page, self.cont_image, self.cont_column)

    def on_sign_in(self, e):
        self.animations(170)
        login_page(self.page, self.cont_image, self.cont_column)

    def vote_login(self, e):
        self.animations(250)
        vote_login_page(self.page, self.cont_image, self.cont_column)

    def build(self):
        def on_hover_color(e):
            if self.text != 'Connect Server':
                e.control.bgcolor = "#0369a1" if e.data == "true" else "#0ea5e9"
                e.control.update()

        self.button_container = ft.Container(
            width=300,
            height=50,
            border_radius=10,
            bgcolor="#0ea5e9",
            alignment=ft.alignment.center,
            on_hover=on_hover_color,
            content=self.text_val,
            animate=ft.animation.Animation(100, ft.AnimationCurve.DECELERATE)
        )

        if self.text == 'Connect Server':
            self.button_container.bgcolor = "#bae6fd"
            self.button_container.tooltip = "Disabled"
            self.button_container.opacity = 0.5
            self.text_val.color = '#0369a1'
        elif self.text == "Create Account":
            self.button_container.on_click = self.on_create_account
        elif self.text == "Sign In":
            self.button_container.on_click = self.on_sign_in
        elif self.text == 'Vote':
            self.button_container.on_click = self.vote_login

        return self.button_container


def menu_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    global cont_image, cont_column
    cont_image = content_image
    cont_column = content_column

    if start is True:
        list_menu_button = [
            MenuButtons(page, "Create Account"),
            MenuButtons(page, "Connect Server"),
        ]
    else:
        ee.election_start_scr()
        list_menu_button = [
            MenuButtons(page, "Sign In"),
            MenuButtons(page, "Vote"),
        ]

    content_column.controls = [
        ft.Column(
            list_menu_button,
            width=250,
            spacing=20,
        )
    ]

    page.update()
