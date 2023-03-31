import flet as ft


def election_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Election"

    page.update()
