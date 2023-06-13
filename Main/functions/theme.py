import flet as ft


def start_theme(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.theme.Theme(color_scheme_seed="blue")
    page.update()
