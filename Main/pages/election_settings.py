import flet as ft
import pandas as pd

from .category import category_dialogs
import Main.service.scr.election_scr as ee
from .election_options import category_order, forgot_code, generate_result, result_view_dialogs
from .settings_options import help_dialogs
from .summary_view import summary_view_page
from ..functions.dialogs import message_dialogs
from ..functions.download import download_nomination, download_result
from ..service.scr.loc_file_scr import file_data
import Main.service.user.login_enc as cc

ele_option_data_update = None


class ElectionSettingsMenu:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.final_nomination_list = None
        self.generate_result = None
        self.download_result = None
        self.download_nomination = None
        self.view_result = None
        self.summary_view_result = None
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

        return self.download_nomination

    def update_in_data(self):
        self.ele_ser_1 = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')

        if not self.ele_ser_1.loc['lock_data'].values[0]:
            self.lock.value = False
        else:
            self.lock.value = True

        if not self.ele_ser_1.loc['final_nomination'].values[0]:
            self.download_nomination.disabled = True
        else:
            self.download_nomination.disabled = False

        if pd.isna(self.ele_ser_1.loc['code'].values[0]):
            self.forgot_passcode.disabled = True
        else:
            self.forgot_passcode.disabled = False

        if not self.ele_ser_1.loc['lock_data'].values[0]:
            self.vote_button.disabled = True
            self.final_nomination_list.disabled = True
        else:
            self.vote_button.disabled = False
            self.final_nomination_list.disabled = False

        if self.ele_ser_1.loc["vote_option"].values[0]:
            self.vote_switch.value = True
        else:
            self.vote_switch.value = False

        if self.ele_ser_1.loc["completed"].values[0]:
            self.lock_election.disabled = True
            self.generate_result.disabled = False
        else:
            self.generate_result.disabled = True
            self.lock_election.disabled = False

        if self.ele_ser_1.loc["result"].values[0]:
            self.view_result.disabled = False
            self.download_result.disabled = False
            self.summary_view_result.disabled = False
        else:
            self.view_result.disabled = True
            self.download_result.disabled = True
            self.summary_view_result.disabled = True

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

        return self.vote_button

    def generate_result_option(self):

        self.generate_result = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Generate result",
                        font_family='Verdana',
                    ),
                    on_click=lambda _: generate_result(self.page),
                    trailing=self.next_icon,
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        return self.generate_result

    def view_result_option(self):

        self.view_result = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        font_family='Verdana',
                        value=f"View result",
                    ),
                    trailing=self.next_icon,
                    on_click=lambda _: result_view_dialogs(self.page),
                ),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        return self.view_result

    def summary_view_result_option(self):

        self.summary_view_result = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Summary view result",
                        font_family='Verdana',
                    ),
                    trailing=self.next_icon,
                    on_click=lambda _: summary_view_page(self.page),
                ),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        return self.summary_view_result

    def download_result_option(self):

        self.download_result = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        font_family='Verdana',
                        value=f"Download result",
                    ),
                    trailing=self.next_icon,
                    on_click=lambda _: download_result(self.page),
                ),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3.5),
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        return self.download_result

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

    if cc.teme_data[2] == True:
        settings_options = [
            ft.Row(height=3),
            category_option,
            option_menu_ele.lock_election_option(),
            option_menu_ele.final_nomination_list_option(),
            option_menu_ele.download_nomination_option(),
            option_menu_ele.vote_option(),
            option_menu_ele.generate_result_option(),
            option_menu_ele.view_result_option(),
            option_menu_ele.summary_view_result_option(),
            option_menu_ele.download_result_option(),
            option_menu_ele.forgot_passcode_option(),
            option_menu_ele.help_option(),
        ]
    else:
        settings_options = [
            ft.Row(height=3),
            category_option,
            option_menu_ele.download_nomination_option(),
            option_menu_ele.view_result_option(),
            option_menu_ele.summary_view_result_option(),
            option_menu_ele.help_option(),
        ]

    main_column.controls = [
        ft.Container(
            content=ft.Column(
                controls=settings_options,
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            margin=ft.margin.only(left=5, right=5),
            expand=True,
        )
    ]

    page.splash = None
    page.update()
    option_menu_ele.update_in_data()


def update_election_set():
    ele_option_data_update.update_in_data()
