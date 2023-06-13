import flet as ft


def snack_bar1(page: ft.Page, text: str):

    # Functions
    def close(e):
        page.snack_bar = snack_bar_1
        page.snack_bar.open = False
        page.update()

    # SnackBar data
    snack_bar_1 = ft.SnackBar(
        content=ft.Text(f"{text}", font_family='Verdana',),
        action="Close",
        on_action=close,
        action_color=ft.colors.BLUE,
    )

    # open snackBar
    page.snack_bar = snack_bar_1
    page.snack_bar.open = True
    page.update()
