import flet as ft
import pandas as pd

from ..authentication.encrypter.encryption import decrypter
from ..authentication.scr.check_installation import path
from ..authentication.scr.loc_file_scr import file_path


def profile_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    import Main.authentication.user.login_enc as cc
    title_text.value = "My Profile"

    main_profile_text = ft.Text(
        value="My Profile",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    def edit_profile_fun(e):
        from .staff_edit import staff_edit_page
        content_column.clean()
        content_column.update()
        staff_edit_page(page, content_column, title_text, cc.teme_data[0], True)

    edit_profile_button = ft.FloatingActionButton(
        icon=ft.icons.EDIT_ROUNDED,
        tooltip="Edit Profile",
        on_click=edit_profile_fun,
    )

    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    staff_login_df = pd.read_json(path + file_path['admin_login_data'], orient='table')

    permission_icon = ft.Icon(
        size=40,
        scale=1.5,
    )

    last_login_text = ft.Text(
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    date_1 = ''
    read_val = str(staff_login_df[staff_login_df.id == cc.teme_data[0]].values[0][1])
    for i in range(10):
        date_1 += read_val[i]
    last_login_text.value = f"{date_1} - {str(staff_login_df[staff_login_df.id == cc.teme_data[0]].values[0][2])}"

    if staff_df[staff_df.id == cc.teme_data[0]].values[0][4] == True:
        permission_icon.name = ft.icons.DONE_ALL_ROUNDED
        permission_icon.color = ft.colors.GREEN_700
    else:
        permission_icon.name = ft.icons.CLOSE_ROUNDED
        permission_icon.color = ft.colors.RED_700

    profile_column_data = ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                value="Username: ",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value="Mail id: ",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value="Password: ",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value="Permission: ",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value="Last Login: ",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        width=200,
                        spacing=40,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                value=f"{decrypter(staff_df[staff_df.id == cc.teme_data[0]].values[0][1])}",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value=f"{decrypter(staff_df[staff_df.id == cc.teme_data[0]].values[0][2])}",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value=f"{decrypter(staff_df[staff_df.id == cc.teme_data[0]].values[0][3])}",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            permission_icon,
                            last_login_text,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=40,
                    ),
                    ft.Row(
                        height=20
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        spacing=30,
        width=600,
    )

    content_column.controls = [
        ft.Row(
            [
                ft.Row(
                    [
                        main_profile_text,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        edit_profile_button,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
        ),
        ft.Divider(
            thickness=3,
            height=5,
        ),
        ft.Column(
            [
                ft.Row(
                    height=40,
                ),
                profile_column_data,
                ft.Row(
                    height=20,
                )
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]

    page.update()
