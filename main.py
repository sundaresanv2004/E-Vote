import flet as ft

from Main.functions.theme import start_theme
from Main.functions.window_actions import window_at_start, window_on_resize
from Main.service.scr.check_installation import installation_requirement
from Main.pages.menu import menu_page


def main(page: ft.Page):
    # minimum width and height of the window.
    page.window_min_width = 700
    page.window_min_height = 550

    # title
    page.title = "E Vote"

    # center
    page.window_center()

    # on resize
    window_at_start(page)

    page.on_window_event = lambda e: window_on_resize(page)

    # theme
    start_theme(page)

    content_image = ft.Container(
        image_src='Main/assets/images/content_image-1.png',
        image_fit=ft.ImageFit.FIT_HEIGHT,
        height=370,
        animate=ft.Animation(600, ft.AnimationCurve.DECELERATE)
    )

    content_column = ft.Column(
        width=450,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    bg_container = ft.Container(
        image_src="Main/assets/images/Background-1.png",
        image_fit=ft.ImageFit.COVER,
        margin=-10,
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Container(
            width=450,
            height=550,
            border_radius=15,
            bgcolor='#44CCCCCC',
            blur=ft.Blur(30, 15, ft.BlurTileMode.MIRROR),
            content=ft.Column(
                [
                    content_image,
                    content_column,
                ],
                width=450,
                height=550,
            )
        )
    )

    page.add(bg_container)
    menu_page(page, content_image, content_column)


if __name__ == '__main__':
    installation_requirement()
    ft.app(
        target=main,
    )
