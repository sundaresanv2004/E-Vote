import flet as ft


def settings_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Settings"

    settings_column_data = ft.Column(
        [
            ft.Row(
                height=5
            ),

        ]
    )

    content_column.controls = [
        settings_column_data,
    ]

    content_column.scroll = ft.ScrollMode.ADAPTIVE
    content_column.alignment = ft.MainAxisAlignment.START
    page.update()
