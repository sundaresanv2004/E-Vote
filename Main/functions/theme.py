import pandas as pd
import flet as ft

from Main.authentication.files.settings_write import main_theme_on_change
from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path
import Main.authentication.user.login_enc as cc


current_theme_mod = None


def start_theme(page: ft.Page):
    global current_theme_mod
    settings_df = pd.read_json(path + file_path['settings'], orient='table')
    page.theme_mode = settings_df.loc['Theme Mode'].values[0]
    page.update()
    if page.theme_mode == "light":
        current_theme_mod = "light"
    else:
        current_theme_mod = "dark"


class ThemeIcon(ft.UserControl):

    def __init__(self, page):
        super().__init__()
        global current_theme_mod
        self.page = page
        self.theme_icon = ft.IconButton(
            icon_color=ft.colors.BLUE,
            icon_size=30,
            on_click=self.change_theme,
        )

        if current_theme_mod == 'light':
            self.theme_icon.icon = ft.icons.DARK_MODE
            self.theme_icon.tooltip = "Dark mode"
        else:
            self.theme_icon.icon = ft.icons.SUNNY
            self.theme_icon.tooltip = "Light mode"

    def change_theme(self, e):
        global current_theme_mod
        if current_theme_mod != 'light':
            self.theme_icon.icon = ft.icons.DARK_MODE
            self.theme_icon.tooltip = "Dark mode"
            current_theme_mod = 'light'
            self.page.theme_mode = 'light'
            main_theme_on_change("light")
        else:
            self.theme_icon.icon = ft.icons.SUNNY
            self.theme_icon.tooltip = "Light mode"
            current_theme_mod = 'dark'
            self.page.theme_mode = 'dark'
            main_theme_on_change("dark")

        self.theme_icon.update()
        self.page.update()

    def build(self):

        return self.theme_icon


class UserThemeIcon(ft.UserControl):

    def __init__(self, page):
        super().__init__()
        global current_theme_mod
        self.page = page
        self.user_theme = cc.teme_data[3]
        self.theme_icon = ft.IconButton(
            icon_size=30,
            on_click=self.change_theme,
        )

        if self.user_theme == 'light':
            self.theme_icon.icon = ft.icons.DARK_MODE
            self.theme_icon.tooltip = "Dark mode"
            self.page.theme_mode = 'light'
        elif self.user_theme == 'dark':
            self.theme_icon.icon = ft.icons.SUNNY
            self.theme_icon.tooltip = "Light mode"
            self.page.theme_mode = 'dark'
        else:
            if current_theme_mod == 'light':
                self.theme_icon.icon = ft.icons.DARK_MODE
                self.theme_icon.tooltip = "Dark mode"
                self.page.theme_mode = 'light'
                self.user_theme = 'light'
            else:
                self.theme_icon.icon = ft.icons.SUNNY
                self.theme_icon.tooltip = "Light mode"
                self.page.theme_mode = 'dark'
                self.user_theme = 'dark'

    def change_theme(self, e):
        from Main.authentication.files.write_files import theme_on_change
        if self.user_theme == 'light':
            self.theme_icon.icon = ft.icons.SUNNY
            self.theme_icon.tooltip = "Light mode"
            self.user_theme = 'dark'
            self.page.theme_mode = 'dark'
        elif self.user_theme == 'dark':
            self.theme_icon.icon = ft.icons.DARK_MODE
            self.theme_icon.tooltip = "Dark mode"
            self.user_theme = 'light'
            self.page.theme_mode = 'light'
        else:
            if current_theme_mod == 'light':
                self.theme_icon.icon = ft.icons.DARK_MODE
                self.theme_icon.tooltip = "Dark mode"
                self.page.theme_mode = 'light'
                self.user_theme = 'light'
            else:
                self.theme_icon.icon = ft.icons.SUNNY
                self.theme_icon.tooltip = "Light mode"
                self.page.theme_mode = 'dark'
                self.user_theme = 'dark'

        theme_on_change(self.user_theme)
        self.theme_icon.update()
        self.page.update()

    def build(self):

        return self.theme_icon
