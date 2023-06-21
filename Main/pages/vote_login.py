import os
from time import sleep
import flet as ft
import pandas as pd

from ..service.scr.check_installation import path
from ..service.scr.loc_file_scr import file_path, file_data
import Main.service.scr.election_scr as ee
from ..service.user.verification import verification_page


def vote_login_page(page: ft.Page, content_image: ft.Container, content_column: ft.Column):
    def on_hover_color(e):
        e.control.bgcolor = "#0369a1" if e.data == "true" else "#0ea5e9"
        e.control.update()

    def back(e):
        from .menu import menu_page
        content_image.height = 370
        content_image.update()
        sleep(0.3)
        content_column.clean()
        page.update()
        menu_page(page, content_image, content_column)

    def vote_login_check_fun(e):
        if len(code_entry.value) != 0:
            if verification_page(code_entry.value):
                code_entry.error_text = None
                button_container.content = ft.ProgressRing(color=ft.colors.WHITE)
                content_column.disabled = True
                button_container.opacity = 0.5
                button_container.bgcolor = '#295361'
                page.update()
                sleep(2)
                page.clean()
                page.update()
                ee.election_start_scr()
                election_data_loc = rf'\{file_data["vote_data"]}\{file_data["election_data"]}'
                final_category_data1 = pd.read_csv(
                    ee.current_election_path + rf'\{file_data["vote_data"]}\{file_data["final_category"]}')
                if not os.path.exists(ee.current_election_path + election_data_loc):
                    election_data1 = pd.DataFrame(columns=list(final_category_data1['category']))
                    election_data1.to_json(ee.current_election_path + election_data_loc, orient='table', index=False)
                from .vote_home import vote_start_page
                vote_start_page(page)
            else:
                code_entry.error_text = "Invalid Code"
                code_entry.focus()
                code_entry.update()
        else:
            code_entry.error_text = "Enter the Code"
            code_entry.focus()
            code_entry.update()

    button_container = ft.Container(
        height=50,
        width=330,
        bgcolor="#0ea5e9",
        border_radius=10,
        on_hover=on_hover_color,
        content=ft.Text(
            value="Vote",
            size=20,
            font_family='Verdana',
            weight=ft.FontWeight.W_400,
            color=ft.colors.WHITE,
        ),
        alignment=ft.alignment.center,
        animate=ft.animation.Animation(100, ft.AnimationCurve.DECELERATE),
        on_click=vote_login_check_fun,
    )

    # Input Fields
    code_entry = ft.TextField(
        hint_text="Enter the Code",
        width=330,
        filled=False,
        prefix_icon=ft.icons.LOCK_ROUNDED,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.colors.BLACK,
        password=True,
        autofocus=True,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        on_submit=vote_login_check_fun,
    )

    vote_waring_text = ft.Text(
        size=20,
        color=ft.colors.ERROR,
        font_family='Verdana',
    )

    settings_df = pd.read_json(path + file_path['settings'], orient='table')
    ele_ser_10 = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')

    if not pd.isna(settings_df.loc['Election'].values[0]):
        if not ele_ser_10.loc['vote_option'].values[0]:
            code_entry.disabled = True
            button_container.bgcolor = "#bae6fd"
            button_container.tooltip = "Disabled"
            button_container.opacity = 0.5
            button_container.on_hover = None
            vote_waring_text.value = 'This option is disabled.'

    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Vote",
                            color='#0c4a6e',
                            size=30,
                            font_family='Verdana',
                            weight=ft.FontWeight.W_800,
                        ),
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        code_entry,
                        button_container,
                    ],
                    width=450,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                ),
                ft.Row(
                    [
                        vote_waring_text
                    ],
                    width=450,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            width=450,
            height=240,
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=15,
        ),
        ft.Container(
            content=ft.Row(
                [
                    ft.TextButton(
                        text="Back",
                        icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        on_click=back,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                width=450,
            ),
            bgcolor='#44CCCCCC',
            blur=ft.Blur(50, 50, ft.BlurTileMode.MIRROR),
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
        )
    ]

    page.update()
