import flet as ft

import Main.functions.theme as tt
import Main.authentication.user.login_enc as cc


def staff_sidebar(page: ft.Page):
    pass


def admin_sidebar(page: ft.Page):
    def expand(e):
        sidebar_icon.icon = ft.icons.ARROW_LEFT_ROUNDED
        admin_option_rail.extended = True
        sidebar_icon.tooltip = "Shrink"
        sidebar_icon.on_click = shrink
        page.update()

    def shrink(e):
        sidebar_icon.icon = ft.icons.ARROW_RIGHT_ROUNDED
        admin_option_rail.extended = False
        sidebar_icon.tooltip = "Expand"
        sidebar_icon.on_click = expand
        page.update()

    def profile_icon_on_click(e):
        admin_option_rail.selected_index = 3
        clicked(3)

    def clicked(e):
        page.splash = ft.ProgressBar()
        content_column.scroll = None
        if e != 6:
            content_column.clean()
        page.update()
        if e == 0:
            from Main.pages.home import home_page
            page.splash = None
            page.update()
            home_page(page, content_column, admin_option_rail, page_title_text)
        elif e == 1:
            from Main.pages.candidate_home import candidate_home_page
            page.splash = None
            page.update()
            candidate_home_page(page, content_column, page_title_text)
        elif e == 2:
            from Main.pages.staff_home import staff_home_page
            page.splash = None
            page.update()
            staff_home_page(page, content_column, page_title_text)
        elif e == 3:
            from Main.pages.profile import profile_home_page
            page.splash = None
            page.update()
            profile_home_page(page, content_column, page_title_text)
        elif e == 4:
            from Main.pages.election_home import election_home_page
            page.splash = None
            page.update()
            election_home_page(page, content_column, page_title_text)
        elif e == 5:
            from Main.pages.settings_home import settings_home_page
            page.splash = None
            page.update()
            settings_home_page(page, content_column, page_title_text)
        elif e == 6:
            from main import main
            from Main.functions.dialogs import loading_dialogs
            page_title_text.value = "Loging out..."
            loading_dialogs(page, "Loging out...", 4)
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
    # AppBar
    appbar = ft.AppBar(
        leading=sidebar_icon,
        title=page_title_text,
        leading_width=50,
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.CircleAvatar(
                bgcolor=ft.colors.ON_SECONDARY,
                content=ft.IconButton(
                    icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                    icon_size=25,
                    tooltip="Profile",
                    on_click=profile_icon_on_click,
                ),
            ),
            ft.Text(" "),
            ft.Text(
                value=cc.teme_data[1].capitalize(),
                weight=ft.FontWeight.BOLD,
                size=15,
            ),
            ft.Text("   "),
            tt.UserThemeIcon(page)
        ],
    )

    content_column = ft.Column(
        expand=True,
    )

    # NavigationRail
    admin_option_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.SELECTED,
        extended=False,
        min_width=80,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME_ROUNDED,
                label="Home",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SUPERVISED_USER_CIRCLE_OUTLINED,
                selected_icon=ft.icons.SUPERVISED_USER_CIRCLE,
                label="Candidate",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                selected_icon=ft.icons.ADMIN_PANEL_SETTINGS,
                label="Staff",
                padding=5,
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ACCOUNT_CIRCLE_OUTLINED,
                selected_icon=ft.icons.ACCOUNT_CIRCLE,
                label="Profile",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.HOW_TO_VOTE_OUTLINED,
                selected_icon=ft.icons.HOW_TO_VOTE,
                label="Election",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS,
                label="Settings",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOGOUT,
                selected_icon=ft.icons.LOGOUT,
                label="Logout",
                padding=5,
            ),
        ],
        on_change=lambda e: clicked(e.control.selected_index),
    )

    page.add(
        appbar,
        ft.Row(
            [
                admin_option_rail,
                ft.VerticalDivider(width=1),
                content_column,
            ],
            expand=True,
        )
    )
    clicked(0)
    page.update()
