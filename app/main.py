import flet as ft

from Main.authentication.scr.check_installation import installation_requirement
from Main.functions.theme import start_theme
from Main.functions.window_close import close_true
from Main.pages.menu import menu_page


def main(page: ft.Page):
    # minimum width and height of the window.
    page.window_min_width = 900
    page.window_min_height = 550

    # tittle
    page.title = "E Vote"

    # center
    page.window_center()

    # at_close
    def at_close_event(e):
        if e.data == "close":
            close_true(page)

    # ask question at close [True, False]
    page.window_prevent_close = False
    page.on_window_event = at_close_event

    # theme
    start_theme(page)

    menu_container = ft.Container(
        width=700,
        height=450,
        border=ft.border.all(1, ft.colors.SECONDARY),
        border_radius=15,
        animate=ft.animation.Animation(900, ft.AnimationCurve.DECELERATE)
    )

    menu_column = ft.Column(
        [
            ft.Row(
                [
                    menu_container,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(menu_column)
    menu_page(page, menu_container)

    # from Main.pages.sidebar_options import admin_sidebar
    # admin_sidebar(page)


if __name__ == "__main__":
    installation_requirement()
    ft.app(
        target=main,
    )
