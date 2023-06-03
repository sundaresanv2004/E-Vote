import flet as ft

from Main.authentication.scr.check_installation import installation_requirement, os_sys, path
from Main.functions.theme import start_theme
from Main.functions.window_close import close_true
from Main.functions.window_resize import window_maximized, window_size_at_start
from Main.pages.menu import menu_page
from Main.pages.unsupported import UnsupportedPage


def main(page: ft.Page):
    # minimum width and height of the window.
    page.window_min_width = 900
    page.window_min_height = 550

    # title
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

    # on resize
    window_size_at_start(page)

    def at_max_min(e):
        window_maximized(page)

    page.on_window_event = at_max_min

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
    # admin_sidebar(page, True)

    # from Main.pages.vote_home import vote_page
    # vote_page(page)


def unsupported_page(page: ft.Page):
    # Width and height of the window.
    page.window_width = 700
    page.window_height = 440

    # Windows Center
    page.window_center()

    # Windows options
    page.window_always_on_top = True
    page.window_title_bar_buttons_hidden = True
    page.window_title_bar_hidden = True
    page.window_resizable = False

    # Container
    menu_container = ft.Container(
        content=UnsupportedPage(page),
        expand=True,
    )

    # Add to Page
    page.add(
        menu_container
    )
    page.update()


if __name__ == "__main__":
    if os_sys == "Windows":
        installation_requirement()
        ft.app(
            target=main,
            assets_dir=path,
            upload_dir=path,
        )
    else:
        ft.app(
            target=unsupported_page,
        )
