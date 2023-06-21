import flet as ft
import pandas as pd

from .category import category_dialogs
import Main.service.scr.election_scr as ee
from .election_options import category_order, forgot_code
from .settings_options import help_dialogs
from ..functions.dialogs import message_dialogs
from ..functions.download_nomination import download_nomination
from ..service.scr.loc_file_scr import file_data

ele_option_data_update = None


class ElectionSettingsMenu:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.final_nomination_list = None
        self.download_nomination = None
        self.lock_election = None
        self.forgot_passcode = None
        self.vote_button = None
        self.help = None
        self.lock = ft.Switch(on_change=self.on_lock_click)
        self.vote_switch = ft.Switch(on_change=self.on_vote_click)
        self.ele_ser_1 = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        self.next_icon = ft.Icon(
            name=ft.icons.NAVIGATE_NEXT_ROUNDED,
            size=25,
        )

    def on_lock_click(self, e):
        from .election_options import passcode_election, lock_unlock_data
        if pd.isna(self.ele_ser_1.loc['code'].values[0]):
            if self.lock.value:
                passcode_election(self.page, self.lock)
        else:
            lock_unlock_data(self.page, self.lock)

        self.page.update()

    def lock_election_option(self):

        self.lock_election = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Lock Data",
                        font_family='Verdana',
                    ),
                    trailing=self.lock,
                ),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                padding=ft.padding.symmetric(vertical=3.5),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        if not self.ele_ser_1.loc['lock_data'].values[0]:
            self.lock.value = False
        else:
            self.lock.value = True

        return self.lock_election

    def final_nomination_list_option(self):

        self.final_nomination_list = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Generate nomination list",
                        font_family='Verdana',
                    ),
                    trailing=self.next_icon,
                    on_click=lambda _: category_order(self.page),
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )
        
        if not self.ele_ser_1.loc['lock_data'].values[0]:
            self.final_nomination_list.disabled = True
        else:
            self.final_nomination_list.disabled = False

        return self.final_nomination_list

    def download_nomination_option(self):

        self.download_nomination = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Download nomination list",
                        font_family='Verdana',
                    ),
                    on_click=lambda _: download_nomination(self.page),
                    trailing=self.next_icon,
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        if not self.ele_ser_1.loc['final_nomination'].values[0]:
            self.download_nomination.disabled = True
        else:
            self.download_nomination.disabled = False

        return self.download_nomination

    def update_in_data(self):
        self.ele_ser_1 = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        if not self.ele_ser_1.loc['lock_data'].values[0]:
            self.final_nomination_list.disabled = True
            self.on_vote_click('e')
        else:
            self.final_nomination_list.disabled = False
        if not self.ele_ser_1.loc['final_nomination'].values[0]:
            self.download_nomination.disabled = True
        else:
            self.download_nomination.disabled = False
        self.page.update()

    def on_vote_click(self, e):
        if not (self.ele_ser_1.loc['lock_data'].values[0] and self.ele_ser_1.loc['final_nomination'].values[0]):
            message_dialogs(self.page, "Enable Vote")
            self.vote_switch.value = False
            self.page.update()
        else:
            from ..service.files.vote_settings_write import vote_on
            vote_on(self.vote_switch.value)

    def vote_option(self):
        self.vote_button = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        font_family='Verdana',
                        value=f"Vote",
                    ),
                    trailing=self.vote_switch,
                ),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                padding=ft.padding.symmetric(vertical=3.5),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        if self.ele_ser_1.loc["vote_option"].values[0]:
            self.vote_switch.value = True
        else:
            self.vote_switch.value = False

        return self.vote_button

    def forgot_passcode_option(self):
        self.forgot_passcode = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Forgot code?",
                        font_family='Verdana',
                    ),
                    trailing=self.next_icon,
                    on_click=lambda _: forgot_code(self.page),
                ),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        return self.forgot_passcode

    def help_option(self):
        self.help = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Help",
                        font_family='Verdana',
                    ),
                    on_click=lambda _: help_dialogs(self.page),
                    trailing=self.next_icon,
                ),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        return self.help


def election_settings_page(page: ft.Page, main_column: ft.Column):
    global ele_option_data_update
    option_menu_ele = ElectionSettingsMenu(page)
    ele_option_data_update = option_menu_ele

    category_option = ft.Card(
        ft.Container(
            ft.ListTile(
                title=ft.Text(
                    value=f"Category",
                    font_family='Verdana',
                ),
                trailing=ft.Icon(
                    name=ft.icons.NAVIGATE_NEXT_ROUNDED,
                    size=25,
                ),
                on_click=lambda _: category_dialogs(page),
            ),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            padding=ft.padding.symmetric(vertical=3.5),
            border_radius=10,
        ),
        elevation=0,
        color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
    )

    main_column.controls = [
        ft.Column(
            [
                ft.Row(height=3),
                category_option,
                option_menu_ele.lock_election_option(),
                option_menu_ele.final_nomination_list_option(),
                option_menu_ele.download_nomination_option(),
                option_menu_ele.vote_option(),
                option_menu_ele.forgot_passcode_option(),
                option_menu_ele.help_option(),
            ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE
        )
    ]

    page.splash = None
    page.update()


def update_election_set():
    ele_option_data_update.update_in_data()
