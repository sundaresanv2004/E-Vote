import flet as ft
import numpy as np
import pandas as pd

import Main.authentication.scr.election_scr as ee
from Main.authentication.scr.loc_file_scr import file_data

obj = None


def from_page_check():
    obj.check_date()


class ElectionData:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.from_date_text = ft.Text(size=20)
        self.to_date_text = ft.Text(size=20)
        self.lock_switch = None
        self.lock_container_option = None
        self.registration_date_option = None
        self.registration_container_option = None
        self.election_date_option = None
        self.registration_switch = ft.Switch(on_change=self.registration_on_change)
        self.page = page
        self.ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        self.election_title_option = None
        self.manage_category_option = None

    def category_container(self):
        self.manage_category_option = ft.Container(
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
                            )
                        ]
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            border_radius=10,
            ink=True,
            on_click=lambda e: print("clicked!"),
            border=ft.border.all(0.3, ft.colors.SECONDARY)
        )
        return self.manage_category_option

    def election_title(self):
        self.election_title_option = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Election Name:",
                                size=20,
                            ),
                            ft.Text(
                                value=f"{self.ele_ser.loc['election-name'].values[0]}",
                                size=20,
                            ),
                        ],
                        spacing=20,
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                text="Edit",
                                icon=ft.icons.EDIT_ROUNDED,
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
            on_click=lambda e: print("clicked!"),
            border_radius=10,
            border=ft.border.all(0.3, ft.colors.SECONDARY)
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
            border_radius=10,
            border=ft.border.all(0.3, ft.colors.SECONDARY)
        )

        if self.ele_ser.loc['registration'].values == False:
            self.registration_switch.value = False
        else:
            self.registration_switch.value = True

        self.check_date()

        return self.registration_container_option

    def lock_container(self):
        self.lock_switch = ft.Switch(
            value=False
        )
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
                            self.lock_switch,
                        ]
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            ink=True,
            on_click=lambda e: print("clicked!"),
            border_radius=10,
            border=ft.border.all(0.3, ft.colors.SECONDARY)
        )

        if self.ele_ser.loc['lock_data'].values == False:
            self.lock_switch.value = False
            self.lock_switch.label = 'Enable'
        else:
            self.lock_switch.value = True
            self.lock_switch.label = 'Disable'

        return self.lock_container_option

    def registration_date_oc_click(self, e):
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
                            ft.TextButton(
                                text="Edit",
                                icon=ft.icons.EDIT_ROUNDED,
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
            border_radius=10,
            border=ft.border.all(0.3, ft.colors.SECONDARY)
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

        try:
            self.registration_date_option.update()
        except AttributeError:
            pass

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


def election_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    global obj
    title_text.value = "Election"
    obj = ElectionData(page)

    main_profile_text = ft.Text(
        value="Election",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
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
        border_radius=10,
        ink=True,
        on_click=lambda e: print("clicked!"),
        border=ft.border.all(0.3, ft.colors.SECONDARY)
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
        border_radius=10,
        ink=True,
        on_click=lambda e: print("clicked!"),
        border=ft.border.all(0.3, ft.colors.SECONDARY)
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
        border_radius=10,
        ink=True,
        on_click=lambda e: print("clicked!"),
        border=ft.border.all(0.3, ft.colors.SECONDARY)
    )

    """
    # TextField
    main_search = ft.TextField(
            hint_text="Search",
            width=450,
            border=ft.InputBorder.OUTLINE,
            border_radius=50,
            border_color=ft.colors.SECONDARY,
            prefix_icon=ft.icons.SEARCH_ROUNDED,
            # on_change=self.disable_save_button,
        )

    dick1 = {"generate result": obj.generate_result_container(), "view result": obj.view_result_container(),
             "election title": obj.election_title(), 'category': obj.category_container(),
             'registration': obj.registration_container(), "registration date": obj.registration_date_container()}"""

    column_data = ft.Column(
        [
            generate_result_option,
            view_result_option,
            view_winners_option,
            obj.election_title(),
            obj.category_container(),
            obj.registration_container(),
            obj.registration_date_container(),
            obj.lock_container(),
        ]
    )

    content_column.controls = [
        column_data,
    ]

    content_column.alignment = ft.MainAxisAlignment.START
    content_column.scroll = ft.ScrollMode.ADAPTIVE
    page.update()
