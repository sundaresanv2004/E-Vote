import flet as ft
import pandas as pd

from ..authentication.scr.check_installation import path
from ..authentication.scr.loc_file_scr import file_path, file_data
from ..functions.date_time import current_time
import Main.authentication.scr.election_scr as ee
from ..functions.dialogs import message_dialogs


def home_page(page: ft.Page, content_column: ft.Column, rail_name: ft.NavigationRail, title_text: ft.Text):
    import Main.authentication.user.login_enc as cc
    title_text.value = "Home"

    # Functions
    def staff_view(e):
        page.splash = ft.ProgressBar()
        page.update()
        rail_name.selected_index = 2
        from Main.pages.staff_home import staff_home_page
        content_column.clean()
        page.splash = None
        content_column.scroll = None
        page.update()
        staff_home_page(page, content_column, title_text)

    def staff_add(e):
        page.splash = ft.ProgressBar()
        page.update()
        rail_name.selected_index = 2
        from Main.pages.staff_add import staff_add_page
        content_column.clean()
        page.splash = None
        content_column.scroll = None
        page.update()
        staff_add_page(page, content_column, title_text)

    def candidate_view(e):
        page.splash = ft.ProgressBar()
        page.update()
        rail_name.selected_index = 1
        from .candidate_home import candidate_home_page
        content_column.clean()
        page.splash = None
        content_column.scroll = None
        page.update()
        candidate_home_page(page, content_column, title_text)

    def candidate_add(e):
        ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        if not ele_ser.loc['lock_data'].values[0]:
            page.splash = ft.ProgressBar()
            page.update()
            rail_name.selected_index = 1
            from .candidate_add import candidate_add_page
            content_column.clean()
            page.splash = None
            content_column.scroll = None
            page.update()
            candidate_add_page(page, content_column, title_text)
        else:
            message_dialogs(page, "Data is Locked")

    app_data_df = pd.read_json(path + file_path['app_data'], orient='table')
    institution_name_text = ft.Text(
        value=app_data_df[app_data_df.topic == 'institution_name'].values[0][1],
        size=45,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    # Cards
    # candidate info card
    candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')
    student_info_card = ft.Card(
        ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                name=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                                size=40,
                            ),
                            ft.ListTile(
                                title=ft.Text(
                                    value=f"{len(candidate_data_df)}",
                                ),
                                subtitle=ft.Text(
                                    value="No.of Candidates",
                                    color=ft.colors.SECONDARY,
                                ),
                                width=150
                            ),
                            ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT_ROUNDED,
                                items=[
                                    ft.PopupMenuItem(
                                        icon=ft.icons.PERSON_ADD_ALT_1_ROUNDED,
                                        text="Add Candidate",
                                        on_click=candidate_add
                                    ),
                                    ft.PopupMenuItem(
                                        icon=ft.icons.VIEW_LIST_ROUNDED,
                                        text="View Records",
                                        on_click=candidate_view,
                                    ),
                                ]
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=300,
            height=140,
            padding=10,
        )
    )

    # Staff PopupMenuButton
    staff_popup_menu = ft.PopupMenuButton(
        icon=ft.icons.MORE_VERT_ROUNDED,
        items=[
            ft.PopupMenuItem(
                icon=ft.icons.PERSON_ADD_ALT_1_ROUNDED,
                text="Add Staff",
                on_click=staff_add,
            ),
            ft.PopupMenuItem(
                icon=ft.icons.VIEW_LIST_ROUNDED,
                text="View Records",
                on_click=staff_view,
            ),
        ]
    )

    if cc.teme_data[2] != True:
        staff_popup_menu.disabled = True
        staff_popup_menu.tooltip = 'Disabled'

    # staff info card
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    teacher_info_card = ft.Card(
        ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                name=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                                size=40,
                            ),
                            ft.ListTile(
                                title=ft.Text(
                                    value=f"{len(staff_df)}",
                                ),
                                subtitle=ft.Text(
                                    value="No.of Staffs",
                                    color=ft.colors.SECONDARY,
                                ),
                                width=150,
                            ),
                            staff_popup_menu
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=290,
            height=140,
            padding=10,
        )
    )

    # page ui
    setting_df = pd.read_json(path + file_path['settings'], orient='table')
    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        institution_name_text,
                    ],
                    height=170,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(
                                value=f"{current_time}, {cc.teme_data[1].capitalize()}",
                                size=30,
                                italic=True,
                            ),
                            ft.Text(
                                value=f"Selected Election:  {setting_df.loc['Election'].values[0]}",
                                size=25,
                                italic=False,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    margin=30,
                    padding=20,
                    height=150,
                ),
                ft.Container(
                    ft.Row(
                        [
                            student_info_card,
                            teacher_info_card,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    height=200,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    ]

    content_column.scroll = ft.ScrollMode.ADAPTIVE
    page.update()
