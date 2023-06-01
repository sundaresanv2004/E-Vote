from time import sleep

import flet as ft
import pandas as pd

import Main.authentication.user.login_enc as cc
import Main.authentication.scr.election_scr as ee
from ..authentication.scr.loc_file_scr import file_data
from ..functions.dialogs import message_dialogs

obj = None


def from_page_check():
    obj.check_date()


class ElectionData:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.vote_option_option = ft.Container(
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            border_radius=5,
            border=ft.border.all(0.5, ft.colors.SECONDARY)
        )
        self.election_title_text = None
        self.from_date_text = ft.Text(size=20)
        self.to_date_text = ft.Text(size=20)
        self.lock_switch = None
        self.lock_container_option = None
        self.registration_date_option = ft.Container(
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            on_click=self.registration_date_oc_click,
            ink=True,
            border_radius=5,
            border=ft.border.all(0.5, ft.colors.SECONDARY)
        )
        self.final_nomination_option = ft.Container(
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            on_click=self.on_click_nomination_list,
            ink=True,
            border_radius=5,
            border=ft.border.all(0.5, ft.colors.SECONDARY)
        )
        self.download_final_nomination_option = ft.Container(
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            on_click=self.on_download_final_nomination,
            ink=True,
            border_radius=5,
            border=ft.border.all(0.5, ft.colors.SECONDARY)
        )
        self.registration_container_option = None
        self.election_date_option = None
        self.registration_switch = ft.Switch(on_change=self.registration_on_change)
        self.vote_switch = ft.Switch(on_change=self.on_vote_click)
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

        return self.registration_container_option

    def lock_container(self):
        self.lock_container_option = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                size=20,
                                value=f"Lock Data",
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

        if not self.ele_ser.loc['lock_data'].values[0]:
            self.lock.value = False
        else:
            self.lock.value = True

        return self.lock_container_option

    def registration_date_oc_click(self, e):
        sleep(0.1)
        from ..functions.date_time import datetime_field
        datetime_field(self.page)

    def registration_date_container(self):
        self.registration_date_option.content = ft.Row(
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
        )

        if not self.ele_ser.loc['registration'].values:
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

        if not self.ele_ser.loc['registration'].values[0]:
            self.registration_switch.value = False
            self.registration_date_option.disabled = True
        else:
            self.registration_switch.value = True
            self.registration_date_option.disabled = False

        if not self.ele_ser.loc['lock_data'].values[0]:
            self.final_nomination_option.disabled = True
        else:
            self.final_nomination_option.disabled = False

        if not self.ele_ser.loc['final_nomination'].values[0]:
            self.download_final_nomination_option.disabled = True
        else:
            self.download_final_nomination_option.disabled = False

        if self.ele_ser.loc["vote"].values[0]:
            self.vote_switch.value = True
        else:
            self.vote_switch.value = False

        try:
            self.page.update()
        except AttributeError:
            pass

    def on_lock_click(self, e):
        from ..functions.dialogs_election import passcode_election, lock_unlock_data
        if pd.isna(self.ele_ser.loc['code'].values[0]):
            if self.lock.value:
                passcode_election(self.page, self.lock)
        else:
            lock_unlock_data(self.page, self.lock)

        self.page.update()

    def registration_on_change(self, e):
        from ..functions.date_time import datetime_field
        from ..authentication.files.vote_settings_write import registration
        if not self.ele_ser.loc['lock_data'].values[0]:
            a = registration(self.registration_switch.value)
            if self.registration_switch.value:
                self.registration_date_option.disabled = False
                if not datetime_field(self.page):
                    self.registration_switch.value = False
            else:
                self.registration_date_option.disabled = True
        else:
            message_dialogs(self.page, "Data is Locked")
            self.registration_switch.value = False

        self.page.update()

    def on_click_nomination_list(self, e):
        from ..functions.dialogs_election import category_order
        category_order(self.page)

    def final_nomination_list(self):
        self.final_nomination_option.content = ft.Row(
            [
                ft.Row(
                    [
                        ft.Text(
                            value=f"Generate Nomination List",
                            size=20,
                        ),
                    ],
                    spacing=30,
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
                            on_click=self.on_click_nomination_list,
                        )
                    ]
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return self.final_nomination_option

    def on_download_final_nomination(self, e):
        from ..functions.download_data import download_nomination
        download_nomination(self.page)

    def download_final_nomination(self):
        self.download_final_nomination_option.content = ft.Row(
            [
                ft.Row(
                    [
                        ft.Text(
                            value=f"Download Nomination List",
                            size=20,
                        ),
                    ],
                    expand=True,
                    spacing=30,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
                            on_click=self.on_download_final_nomination,
                        )
                    ]
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return self.download_final_nomination_option

    def on_vote_click(self, e):
        if not (self.ele_ser.loc['lock_data'].values[0] and self.ele_ser.loc['final_nomination'].values[0]):
            message_dialogs(self.page, "Enable Vote")
            self.vote_switch.value = False
            self.page.update()
        else:
            from ..authentication.files.vote_settings_write import vote_on
            vote_on(self.vote_switch.value)

    def vote_option(self):
        self.vote_option_option.content = ft.Row(
            [
                ft.Row(
                    [
                        ft.Text(
                            value=f"Vote",
                            size=20,
                        ),
                    ],
                    expand=True,
                    spacing=30,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        self.vote_switch
                    ]
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.check_date()
        return self.vote_option_option


def election_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Election"
    global obj
    obj = ElectionData(page)

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

    list1_data: list = [
        ft.Row(height=5),
        manage_category_option,
        obj.election_title(),
        obj.registration_container(),
        obj.registration_date_container(),
        obj.lock_container(),
        obj.final_nomination_list(),
        obj.download_final_nomination(),
        obj.vote_option(),
    ]

    list2_data: list = [
        ft.Row(height=5),
        generate_result_option,
        view_result_option,
        view_winners_option,
    ]

    tab1_option = ft.Tab(
        text="Election Settings",
        content=ft.Column(
            controls=list1_data,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    )

    tab2_option = ft.Tab(
        text="Result",
        content=ft.Column(
            controls=list2_data,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    )

    tab3_option = ft.Tab(
        text="Help",
        content=ft.Column(
            controls=list2_data,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    )

    tab = ft.Tabs(
        selected_index=0,
        animation_duration=400,
        expand=True,
    )

    if cc.teme_data[2] == False:
        del list2_data[1]
        tab.tabs = [
            tab2_option,
        ]
    else:
        tab.tabs = [
            tab1_option,
            tab2_option,
            tab3_option,
        ]

    content_column.controls = [
        tab,
    ]

    content_column.alignment = ft.MainAxisAlignment.START
    page.update()
