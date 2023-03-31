import flet as ft


def profile_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "My Profile"

    page.update()
