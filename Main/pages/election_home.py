import flet as ft
import pandas as pd

import Main.authentication.user.login_enc as cc
import Main.authentication.scr.election_scr as ee
from ..authentication.scr.loc_file_scr import file_data
from ..functions.dialogs import message_dialogs


def election_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Election"

    def on_category_container(e):
        ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        if not ele_ser.loc['lock_data'].values[0]:
            content_column.scroll = None
            content_column.alignment = ft.MainAxisAlignment.CENTER
            page.update()
            from .category import category_home_page
            content_column.clean()
            content_column.update()
            category_home_page(page, content_column, title_text)
        else:
            message_dialogs(page, "Data is Locked")

    manage_category_option = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Category",
                            size=20,
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
                            on_click=on_category_container,
                        )
                    ]
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=15,
        alignment=ft.alignment.center,
        height=70,
        border_radius=5,
        ink=True,
        on_click=on_category_container,
        border=ft.border.all(0.5, ft.colors.SECONDARY)
    )

    generate_result_option = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Generate Result",
                            size=20,
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
                        )
                    ]
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=15,
        alignment=ft.alignment.center,
        height=70,
        border_radius=5,
        ink=True,
        on_click=lambda e: print("clicked!"),
        border=ft.border.all(0.5, ft.colors.SECONDARY)
    )

    view_result_option = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="View Result",
                            size=20,
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
                        )
                    ]
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=15,
        alignment=ft.alignment.center,
        height=70,
        border_radius=5,
        ink=True,
        on_click=lambda e: print("clicked!"),
        border=ft.border.all(0.5, ft.colors.SECONDARY)
    )

    view_winners_option = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="View Winners",
                            size=20,
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
                        )
                    ]
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=15,
        alignment=ft.alignment.center,
        height=70,
        border_radius=5,
        ink=True,
        on_click=lambda e: print("clicked!"),
        border=ft.border.all(0.5, ft.colors.SECONDARY)
    )

    list1_data: list = [ft.Row(height=5), generate_result_option, view_result_option, view_winners_option,
                        manage_category_option]

    if cc.teme_data[2] == False:
        del list1_data[1]

    column_data = ft.Column(
        controls=list1_data,
    )

    content_column.controls = [
        column_data,
    ]

    content_column.alignment = ft.MainAxisAlignment.START
    content_column.scroll = ft.ScrollMode.ADAPTIVE
    page.update()
