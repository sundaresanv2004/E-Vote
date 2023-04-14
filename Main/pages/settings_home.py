import flet as ft
from time import sleep
import pandas as pd

import Main.authentication.scr.election_scr as ee
from Main.authentication.scr.loc_file_scr import file_data

obj = None


def from_page_check():
    obj.check_date()


class ElectionData:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.election_title_text = None
        self.from_date_text = ft.Text(size=20)
        self.to_date_text = ft.Text(size=20)
        self.lock_switch = None
        self.lock_container_option = None
        self.registration_date_option = None
        self.registration_container_option = None
        self.election_date_option = None
        self.registration_switch = ft.Switch(on_change=self.registration_on_change)
        self.lock = ft.Switch(on_change=self.on_lock_click)
        self.page = page
        self.ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        self.election_title_option = None

    def on_election_title(self, e):
        sleep(0.1)
        from ..functions.dialogs_election import edit_election_name
        edit_election_name(self.page)

    def election_title(self):
        self.election_title_text = ft.Text(
            value=f"{self.ele_ser.loc['election-name'].values[0]}",
            size=20,
        )
        self.election_title_option = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Election Name:",
                                size=20,
                            ),
                            self.election_title_text,
                        ],
                        spacing=20,
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
                                on_click=self.on_election_title,
                            )
                        ]
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            ink=True,
            on_click=self.on_election_title,
            border_radius=5,
            border=ft.border.all(0.5, ft.colors.SECONDARY)
        )
        return self.election_title_option

    def registration_container(self):
        self.registration_container_option = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value=f"Registration",
                                size=20,
                            )
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            self.registration_switch,
                        ]
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            border_radius=5,
            border=ft.border.all(0.5, ft.colors.SECONDARY)
        )

        if self.ele_ser.loc['registration'].values == False:
            self.registration_switch.value = False
        else:
            self.registration_switch.value = True

        self.check_date()

        return self.registration_container_option

    def lock_container(self):
        self.lock_container_option = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value=f"Lock Data",
                                size=20,
                            )
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            self.lock,
                        ]
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            border_radius=5,
            border=ft.border.all(0.5, ft.colors.SECONDARY)
        )

        if self.ele_ser.loc['lock_data'].values == False:
            self.lock.value = False
        else:
            self.lock.value = True

        return self.lock_container_option

    def registration_date_oc_click(self, e):
        sleep(0.1)
        from ..functions.date_time import datetime_field
        datetime_field(self.page)

    def registration_date_container(self):
        self.registration_date_option = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value=f"Registration Date",
                                size=20,
                            ),
                            self.from_date_text,
                            self.to_date_text,
                        ],
                        spacing=30,
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
                                on_click=self.registration_date_oc_click,
                            )
                        ]
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            on_click=self.registration_date_oc_click,
            ink=True,
            border_radius=5,
            border=ft.border.all(0.5, ft.colors.SECONDARY)
        )

        if self.ele_ser.loc['registration'].values == False:
            self.registration_date_option.disabled = True
        else:
            self.registration_date_option.disabled = False

        return self.registration_date_option

    def check_date(self):

        self.ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        if pd.isna(self.ele_ser.loc['registration_from'].values[0]) is True:
            self.from_date_text.value = f"From: -"
            self.to_date_text.value = f"To: -"
        else:
            self.from_date_text.value = f"From: {self.ele_ser.loc['registration_from'].values[0]}"
            self.to_date_text.value = f"To: {self.ele_ser.loc['registration_to'].values[0]}"
        self.election_title_text.value = f"{self.ele_ser.loc['election-name'].values[0]}"
        try:
            self.registration_date_option.update()
        except AttributeError:
            pass

    def on_lock_click(self, e):
        from ..functions.dialogs_election import passcode_election

        if self.registration_switch.value is False:
            passcode_election(self.page, self.lock)
        else:
            pass
        self.page.update()

    def registration_on_change(self, e):
        from ..functions.date_time import datetime_field
        from ..authentication.files.settings_write import registration
        registration(self.registration_switch.value)
        if self.registration_switch.value is True:
            self.registration_date_option.disabled = False
            datetime_field(self.page)
        else:
            self.registration_date_option.disabled = True
        self.page.update()


def settings_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    global obj
    title_text.value = "Settings"
    obj = ElectionData(page)

    settings_column_data = ft.Column(
        [
            ft.Row(
                height=5
            ),
            obj.election_title(),
            obj.registration_container(),
            obj.registration_date_container(),
            obj.lock_container(),
        ]
    )

    content_column.controls = [
        settings_column_data,
    ]

    content_column.scroll = ft.ScrollMode.ADAPTIVE
    content_column.alignment = ft.MainAxisAlignment.START
    page.update()
