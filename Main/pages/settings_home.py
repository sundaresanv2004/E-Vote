import flet as ft

from .settings_admin import SettingsAdminOptions
from .settings_election import SettingsElectionOptions
from .settings_user import SettingsUserOptions


def settings_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Settings"

    # Text & Buttons
    main_title_text = ft.Text(
        value="Settings",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    settings_column_data = ft.Column(
        [
            ft.Row(
                height=10
            ),
            SettingsUserOptions(page, content_column),
            SettingsElectionOptions(page, content_column),
            SettingsAdminOptions(page, content_column),
        ]
    )

    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        main_title_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(
                    height=5,
                    thickness=3,
                ),
                settings_column_data,
            ],
        )
    ]

    content_column.scroll = ft.ScrollMode.ADAPTIVE
    content_column.alignment = ft.MainAxisAlignment.START
    page.update()
