import flet as ft
import pandas as pd

from ..functions.snack_bar import snack_bar1
from ..service.files.settings_write import current_election_name
from ..service.scr.check_installation import path
import Main.service.scr.election_scr as ee
from ..service.scr.loc_file_scr import file_path, file_data
from .settings_options import institution_name_dialogs, new_election_dialogs, help_dialogs, delete_election_dialogs, \
    election_name_dialogs

var_option_data_update = None


class SettingsMenu:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.delete_election = None
        self.election_name = None
        self.help = None
        self.institution_name = None
        self.create_election = None
        self.current_election = None
        self.next_icon = ft.Icon(
            name=ft.icons.NAVIGATE_NEXT_ROUNDED,
            size=25,
        )
        self.election_name_text = ft.Text(font_family='Verdana')
        self.institution_name_text = ft.Text(font_family='Verdana')
        self.current_election_text = ft.Text(font_family='Verdana')
        self.current_election_dropdown = ft.Dropdown(
            hint_text="Choose the Election",
            width=350,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            filled=False,
            text_style=ft.TextStyle(font_family='Verdana'),
            color=ft.colors.BLACK,
            on_change=self.on_change_in_dropdown
        )

    def on_change_in_dropdown(self, e):
        current_election_name(self.current_election_dropdown.value, self.page)

    def institution_name_option(self):
        app_data_sys_df = pd.read_json(path + file_path['app_data'], orient='table')
        self.institution_name_text.value = app_data_sys_df.values[1][1]
        self.institution_name = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Institution Name",
                        font_family='Verdana',
                    ),
                    subtitle=self.institution_name_text,
                    trailing=self.next_icon,
                    on_click=lambda _: institution_name_dialogs(self.page),
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC')
        )

        return self.institution_name

    def election_name_option(self):
        ele_ser1 = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        self.election_name_text.value = ele_ser1.loc['election-name'].values[0]
        self.election_name = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Election Name",
                        font_family='Verdana',
                    ),
                    trailing=self.next_icon,
                    subtitle=self.election_name_text,
                    on_click=lambda _: election_name_dialogs(self.page),
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC')
        )

        return self.election_name

    def crate_election_option(self):
        self.create_election = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Create new election",
                        font_family='Verdana',
                    ),
                    trailing=self.next_icon,
                    on_click=lambda _: new_election_dialogs(self.page),
                ),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                padding=ft.padding.symmetric(vertical=3.5),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        return self.create_election

    def current_election_option(self):
        election_data3 = pd.read_csv(path + file_path["election_data"])
        settings_df1 = pd.read_json(path + file_path['settings'], orient='table')

        temp_list: list = []
        for i in list(election_data3['name']):
            temp_list.append(ft.dropdown.Option(i))

        self.current_election_dropdown.options = temp_list
        self.current_election_dropdown.value = settings_df1.loc['Election'].values[0]
        self.current_election_text.value = settings_df1.loc['Election'].values[0]

        self.current_election = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Curent election",
                        font_family='Verdana',
                    ),
                    subtitle=self.current_election_text,
                    trailing=self.current_election_dropdown,
                ),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                padding=ft.padding.symmetric(vertical=3.5),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        return self.current_election

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

    def delete_election_option(self):
        self.delete_election = ft.Card(
            ft.Container(
                ft.ListTile(
                    title=ft.Text(
                        value=f"Delete election",
                        font_family='Verdana',
                    ),
                    trailing=self.next_icon,
                    on_click=lambda _: delete_election_dialogs(self.page),
                ),
                border_radius=10,
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                padding=ft.padding.symmetric(vertical=3.5),
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
        )

        if len(pd.read_csv(path + file_path["election_data"])) == 1:
            self.delete_election.disabled = True
            self.delete_election.tooltip = 'Disabled'
        else:
            self.delete_election.disabled = False
            self.delete_election.tooltip = None

        return self.delete_election

    def change_in_data(self):
        app_data_sys_df = pd.read_json(path + file_path['app_data'], orient='table')
        self.institution_name_text.value = app_data_sys_df.values[1][1]
        settings_df3 = pd.read_json(path + file_path['settings'], orient='table')
        self.current_election_text.value = settings_df3.loc['Election'].values[0]
        if len(pd.read_csv(path + file_path["election_data"])) == 1:
            self.delete_election.disabled = True
            self.delete_election.tooltip = 'Disabled'
        else:
            self.delete_election.disabled = False
            self.delete_election.tooltip = None
        self.election_name_text.value = settings_df3.loc['Election'].values[0]
        self.page.update()
        snack_bar1(self.page, "Successfully Updated.")


def settings_page(page: ft.Page, main_column: ft.Column):
    global var_option_data_update
    option_menu = SettingsMenu(page)
    var_option_data_update = option_menu

    main_column.controls = [
        ft.Column(
            [
                ft.Row(height=3),
                option_menu.institution_name_option(),
                option_menu.election_name_option(),
                option_menu.crate_election_option(),
                option_menu.current_election_option(),
                option_menu.delete_election_option(),
                option_menu.help_option(),
            ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE
        )
    ]

    page.splash = None
    page.update()


def update_settings_data():
    var_option_data_update.change_in_data()
