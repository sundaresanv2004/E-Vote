import flet as ft
import pandas as pd

import Main.functions.theme as tt
import Main.authentication.user.login_enc as cc

text_data = None


def admin_sidebar(page: ft.Page, staff_val: bool):
    global text_data

    def expand(e):
        sidebar_icon.icon = ft.icons.ARROW_LEFT_ROUNDED
        option_rail.extended = True
        sidebar_icon.tooltip = "Shrink"
        sidebar_icon.on_click = shrink
        page.update()

    def shrink(e):
        sidebar_icon.icon = ft.icons.ARROW_RIGHT_ROUNDED
        option_rail.extended = False
        sidebar_icon.tooltip = "Expand"
        sidebar_icon.on_click = expand
        page.update()

    def profile_icon_on_click(e):
        if staff_val is True:
            option_rail.selected_index = 3
            admin_clicked(3)
        else:
            option_rail.selected_index = 2
            staff_clicked(2)

    def admin_clicked(e):
        old_index = e
        page.splash = ft.ProgressBar()
        content_column.scroll = None
        content_column.alignment = ft.MainAxisAlignment.CENTER
        if e != 6:
            content_column.clean()
        page.update()
        if e == 0:
            from .home import home_page
            page.splash = None
            page.update()
            home_page(page, content_column, option_rail, page_title_text)
        elif e == 1:
            from .candidate_home import candidate_home_page
            page.splash = None
            page.update()
            candidate_home_page(page, content_column, page_title_text)
        elif e == 2:
            from .staff_home import staff_home_page
            page.splash = None
            page.update()
            staff_home_page(page, content_column, page_title_text)
        elif e == 3:
            from .profile import profile_home_page
            page.splash = None
            page.update()
            profile_home_page(page, content_column, page_title_text)
        elif e == 4:
            from .election_home import election_home_page
            page.splash = None
            page.update()
            election_home_page(page, content_column, page_title_text)
        elif e == 5:
            from .settings_home import settings_home_page
            page.splash = None
            page.update()
            settings_home_page(page, content_column, page_title_text)
        elif e == 6:
            from main import main
            from ..functions.dialogs import loading_dialogs
            loading_dialogs(page, "Logging out...", 2)
            page.splash = None
            page.clean()
            page.update()
            main(page)
        page.update()

    def staff_clicked(e):
        old_index = e
        page.splash = ft.ProgressBar()
        content_column.scroll = None
        content_column.alignment = ft.MainAxisAlignment.CENTER
        if e != 5:
            content_column.clean()
        page.update()
        if e == 0:
            from .home import home_page
            page.splash = None
            page.update()
            home_page(page, content_column, option_rail, page_title_text)
        elif e == 1:
            from .candidate_home import candidate_home_page
            page.splash = None
            page.update()
            candidate_home_page(page, content_column, page_title_text)
        elif e == 2:
            from .profile import profile_home_page
            page.splash = None
            page.update()
            profile_home_page(page, content_column, page_title_text)
        elif e == 3:
            from .election_home import election_home_page
            page.splash = None
            page.update()
            election_home_page(page, content_column, page_title_text)
        elif e == 4:
            from .settings_home import settings_home_page
            page.splash = None
            page.update()
            settings_home_page(page, content_column, page_title_text)
        elif e == 5:
            from main import main
            from ..functions.dialogs import loading_dialogs
            loading_dialogs(page, "Logging out...", 2)
            page.splash = None
            page.clean()
            page.update()
            main(page)
        page.update()

    # Icon
    sidebar_icon = ft.IconButton(
        icon=ft.icons.ARROW_RIGHT_ROUNDED,
        tooltip="Expand",
        icon_size=40,
        on_click=expand,
    )

    # Text
    page_title_text = ft.Text(
        size=25
    )

    text_data = ft.Text(
        value=cc.teme_data[1].capitalize(),
        weight=ft.FontWeight.BOLD,
        size=15,
    )

    # AppBar
    appbar = ft.AppBar(
        leading=sidebar_icon,
        title=page_title_text,
        leading_width=50,
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.CircleAvatar(
                            bgcolor=ft.colors.ON_SECONDARY,
                            content=ft.Icon(
                                name=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                                size=25,
                            ),
                        ),
                        text_data,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                ink=True,
                tooltip="Profile",
                on_click=profile_icon_on_click,
                height=50,
                padding=5,
                border_radius=10,
            ),
            ft.Text("   "),
            tt.UserThemeIcon(page)
        ],
    )

    content_column = ft.Column(
        expand=True,
    )

    home_button = ft.NavigationRailDestination(
        icon=ft.icons.HOME_OUTLINED,
        selected_icon=ft.icons.HOME_ROUNDED,
        label="Home",
    )

    candidate_button = ft.NavigationRailDestination(
        icon=ft.icons.SUPERVISED_USER_CIRCLE_OUTLINED,
        selected_icon=ft.icons.SUPERVISED_USER_CIRCLE,
        label="Candidate",
    )

    staff_button = ft.NavigationRailDestination(
        icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
        selected_icon=ft.icons.ADMIN_PANEL_SETTINGS,
        label="Staff",
        padding=5,
    )

    profile_button = ft.NavigationRailDestination(
        icon=ft.icons.ACCOUNT_CIRCLE_OUTLINED,
        selected_icon=ft.icons.ACCOUNT_CIRCLE,
        label="Profile",
    )

    election_button = ft.NavigationRailDestination(
        icon=ft.icons.HOW_TO_VOTE_OUTLINED,
        selected_icon=ft.icons.HOW_TO_VOTE,
        label="Election",
    )

    setting_button = ft.NavigationRailDestination(
        icon=ft.icons.SETTINGS_OUTLINED,
        selected_icon=ft.icons.SETTINGS,
        label="Settings",
    )

    logout_button = ft.NavigationRailDestination(
        icon=ft.icons.LOGOUT,
        selected_icon=ft.icons.LOGOUT,
        label="Logout",
        padding=5,
    )

    admin_list: list = [home_button, candidate_button, staff_button, profile_button, election_button, setting_button,
                        logout_button]
    staff_list: list = [home_button, candidate_button, profile_button, election_button, setting_button, logout_button]

    # NavigationRail
    option_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.SELECTED,
        extended=False,
        min_width=80,
        min_extended_width=200,
        group_alignment=-0.9,
    )

    if staff_val is True:
        option_rail.destinations = admin_list
        option_rail.on_change = lambda e: admin_clicked(e.control.selected_index)
    else:
        option_rail.destinations = staff_list
        option_rail.on_change = lambda e: staff_clicked(e.control.selected_index)

    page.add(
        appbar,
        ft.Row(
            [
                option_rail,
                ft.VerticalDivider(width=1),
                content_column,
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
    )
    if staff_val is True:
        admin_clicked(0)
    else:
        staff_clicked(0)
    page.update()


def update_text(page: ft.Page):
    global text_data
    from Main.authentication.scr.check_installation import path
    from Main.authentication.scr.loc_file_scr import file_path
    from Main.authentication.encrypter.encryption import decrypter

    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    text_data.value = decrypter(staff_df[staff_df.id == cc.teme_data[0]].values[0][1])
    page.update()
