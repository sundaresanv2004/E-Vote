import flet as ft

import Main.functions.theme as tt
from ..authentication.scr.loc_file_scr import app_data, unsupported_message_contents


class UnsupportedPage(ft.UserControl):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.close_icon = ft.IconButton(
            icon=ft.icons.CLOSE_ROUNDED,
            icon_size=25,
            tooltip="Close",
            on_click=self.close,
        )

    def close(self, e):
        self.page.window_destroy()

    def build(self):
        column_content = ft.Column(
            [
                ft.Row(
                    [
                        tt.ThemeIcon(self.page),
                        self.close_icon,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(
                                            value="E",
                                            size=40,
                                            weight=ft.FontWeight.BOLD,
                                            italic=True,
                                        ),
                                        ft.Text(
                                            value="Vote",
                                            size=40,
                                            italic=True,
                                        ),
                                    ],
                                    spacing=15,
                                    width=500,
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Row(
                                    [
                                        ft.Text(
                                            value="Version: ",
                                            size=20,
                                        ),
                                        ft.Text(
                                            value=f"{app_data['version']}",
                                            size=20,
                                        ),
                                    ],
                                    spacing=3,
                                    width=500,
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        ft.Row(
                            height=50,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    value=unsupported_message_contents,
                                    size=20,
                                )
                            ],
                            width=500,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        return column_content
