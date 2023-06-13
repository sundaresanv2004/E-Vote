import flet as ft

import Main.service.user.login_enc as cc
from .staff_add import staff_add_page
from .candidate_add import candidate_add_page

old_data = None


def menubar_page(page: ft.Page):

    main_column = ft.Column(expand=True)

    add_candidate_button = ft.FloatingActionButton(
        icon=ft.icons.PERSON_ADD_ALT_1_ROUNDED,
        tooltip="Add new Candidate",
        on_click=lambda _: candidate_add_page(page),
    )

    add_staff_button = ft.FloatingActionButton(
        icon=ft.icons.PERSON_ADD_ALT_1_ROUNDED,
        tooltip="Add new Staff",
        on_click=lambda _: staff_add_page(page),
    )

    def on_option_click(e):
        page.splash = ft.ProgressBar()
        global old_data

        if e != 5:
            main_column.clean()
            page.update()
            if old_data == 0:
                container.image_src = "Main/assets/images/background-3.png"
                home.icon = None
            elif old_data == 1:
                page.remove(add_candidate_button)
                candidate.icon = None
            elif old_data == 2:
                page.remove(add_staff_button)
                staff.icon = None

            election.icon = None
            settings.icon = None

        old_data = e

        if e == 0:
            container.image_src = "Main/assets/images/background-2.png"
            home.icon = ft.icons.HOME_ROUNDED
            from .home import home_page
            home_page(page, main_column)
        elif e == 1:
            candidate.icon = ft.icons.SUPERVISED_USER_CIRCLE
            from .candidate_home import candidate_home_page
            candidate_home_page(page, main_column)
            page.add(add_candidate_button)
        elif e == 2:
            staff.icon = ft.icons.ADMIN_PANEL_SETTINGS
            from .staff_home import staff_home_page
            staff_home_page(page, main_column)
            page.add(add_staff_button)
        elif e == 3:
            election.icon = ft.icons.HOW_TO_VOTE
        elif e == 4:
            settings.icon = ft.icons.SETTINGS
        elif e == 5:
            from main import main
            from ..functions.dialogs import loading_dialogs
            loading_dialogs(page, "Logging out...", 2)
            page.clean()
            page.splash = None
            page.update()
            main(page)
        page.update()

    home = ft.TextButton(
        text='Home',
        data=0,
        on_click=lambda e: on_option_click(e.control.data)
    )

    candidate = ft.TextButton(
        text="Candidate",
        data=1,
        on_click=lambda e: on_option_click(e.control.data)
    )

    staff = ft.TextButton(
        text="Staff",
        data=2,
        on_click=lambda e: on_option_click(e.control.data)
    )

    election = ft.TextButton(
        text="Election",
        data=3,
        on_click=lambda e: on_option_click(e.control.data)
    )

    settings = ft.TextButton(
        text="Settings",
        data=4,
        on_click=lambda e: on_option_click(e.control.data)
    )

    log_out = ft.TextButton(
        icon=ft.icons.LOGOUT_OUTLINED,
        text="Logout",
        data=5,
        on_click=lambda e: on_option_click(e.control.data)
    )

    row_menu_list = [
        home,
        candidate,
        staff,
        election,
        settings,
    ]

    appbar = ft.Container(
        border_radius=9,
        bgcolor=ft.colors.with_opacity(0.5, '#FFFFFF'),
        blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        content=ft.Text(
                                            value=cc.teme_data[1][0].upper(),
                                            size=25,
                                        ),
                                    ),
                                    ft.Text(
                                        value=cc.teme_data[1].capitalize(),
                                        weight=ft.FontWeight.BOLD,
                                        size=15,
                                    )
                                ]
                            ),
                            tooltip='Profile',
                            margin=5,
                            on_click=lambda _: print('a'),
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
                ft.Row(row_menu_list),
                ft.VerticalDivider(color=ft.colors.PRIMARY, thickness=2),
                log_out,
            ],
            alignment=ft.MainAxisAlignment.END,
            height=50
        ),
        margin=5,

    )

    container = ft.Container(
        image_fit=ft.ImageFit.COVER,
        image_src="Main/assets/images/background-2.png",
        margin=-10,
        expand=True,
        content=ft.Column(
            [
                appbar,
                main_column
            ],
        )
    )

    page.add(container)
    page.update()
    on_option_click(0)