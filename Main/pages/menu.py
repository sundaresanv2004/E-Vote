from time import sleep
import flet as ft
import numpy as np
import pandas as pd

from Main.authentication.scr.check_installation import start, path
import Main.authentication.scr.election_scr as ee
from Main.authentication.scr.loc_file_scr import app_data, file_path, file_data
import Main.functions.theme as tt
from Main.functions.animations import menu_container_animation


def menu_page(page: ft.Page, menu_container: ft.Container):

    # functions
    def get_started_fun(e):
        from Main.pages.start_info import start_info_page
        menu_container.clean()
        page.update()
        menu_container_animation(menu_container)
        sleep(0.2)
        start_info_page(page, menu_container, [])

    def user_login_fun(e):
        from Main.pages.login import login_page
        menu_container.clean()
        page.update()
        menu_container_animation(menu_container)
        sleep(0.2)
        login_page(page, menu_container)

    # Buttons
    # Get Started button
    get_started_button = ft.ElevatedButton(
        text="Get Started",
        height=50,
        width=200,
        on_click=get_started_fun,
    )

    # connection button
    connect_server_button = ft.ElevatedButton(
        text="Connect Server",
        height=50,
        width=200,
        disabled=True,
        tooltip="disabled",
    )

    # login button
    login_button = ft.ElevatedButton(
        text="Log in",
        icon=ft.icons.LOGIN_ROUNDED,
        height=50,
        width=200,
        on_click=user_login_fun,
    )

    # register button
    register_button = ft.ElevatedButton(
        text="Register",
        disabled=True,
        icon=ft.icons.PERSON_ADD_ALT_ROUNDED,
        height=50,
        width=200,
    )

    # vote button
    start_election_button = ft.TextButton(
        text="Start Election now.",
        disabled=True,
        icon=ft.icons.HOW_TO_VOTE_ROUNDED,
    )

    if start is True:
        start_election_button.disabled = True
        start_election_button.tooltip = 'Disabled'
        list_menu_button: list = [get_started_button, connect_server_button]
    else:
        ee.election_start_scr()
        list_menu_button: list = [login_button, register_button]

    # Read files
    setting_df = pd.read_json(path + file_path['settings'], orient='table')
    if setting_df.loc['Election'].values[0] != np.nan:
        election_settings_df = None
        try:
            election_settings_df = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        except TypeError:
            pass
        if election_settings_df is not None:
            if election_settings_df.loc["registration"].values[0] != False:
                register_button.disabled = False
            if election_settings_df.loc["vote"].values[0] != False:
                start_election_button.disabled = False

    # alignment and data
    menu_container_data = ft.Column(
        [
            ft.Row(
                [
                    tt.ThemeIcon(page),
                ],
                alignment=ft.MainAxisAlignment.END,
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
                                spacing=5,
                                width=500,
                                alignment=ft.MainAxisAlignment.START,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        list_menu_button,
                        spacing=25,
                        alignment=ft.MainAxisAlignment.START,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=25,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    start_election_button,
                ],
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    menu_container.content = menu_container_data
    menu_container.padding = 10
    menu_container.update()
    page.update()
