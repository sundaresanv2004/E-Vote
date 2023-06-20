import os

import flet as ft
import pandas as pd

import Main.service.scr.election_scr as ee
from Main.service.scr.loc_file_scr import file_data

election_data_loc = rf'\{file_data["vote_data"]}\{file_data["election_data"]}'


def animation(tittle_bar):
    tittle_bar.margin = ft.margin.only(left=5, right=5, top=5)
    tittle_bar.height = 50
    tittle_bar.width = None
    tittle_bar.update()


def vote_home_page(page: ft.Page):
    final_category_data1 = pd.read_csv(
        ee.current_election_path + rf'\{file_data["vote_data"]}\{file_data["final_category"]}')
    if not os.path.exists(ee.current_election_path + election_data_loc):
        election_data1 = pd.DataFrame(columns=list(final_category_data1['category']))
        election_data1.to_json(ee.current_election_path + election_data_loc, orient='table', index=False)

    main_column = ft.Column(expand=True)

    container = ft.Container(
        image_fit=ft.ImageFit.COVER,
        image_src="Main/assets/images/background-4.png",
        margin=-10,
        expand=True,
        content=ft.Column(
            [
                main_column,
                ft.Row(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    page.add(container)
    page.update()

    vote_page(page, main_column)


def vote_page(page: ft.Page, main_column: ft.Column):
    def on_vote_click(e):
        animation(tittle_bar)


    read_election_data = pd.read_json(ee.current_election_path + election_data_loc, orient='table')
    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        value=f'Vote No: {len(read_election_data) + 1}',
                        font_family='Verdana',
                        size=30,
                        weight=ft.FontWeight.W_700,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=300,
            ),
            ft.Row(height=20),
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.FloatingActionButton(
                                text="Vote",
                                icon=ft.icons.HOW_TO_VOTE_ROUNDED,
                                width=250,
                                on_click=on_vote_click,
                            ),
                            ft.FloatingActionButton(
                                text="Exit",
                                icon=ft.icons.LOGOUT_ROUNDED,
                                width=250,
                            ),
                        ],
                        spacing=20,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=300,
            )

        ],
        width=300,
        height=350,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    tittle_bar = ft.Container(
        width=300,
        height=350,
        border_radius=15,
        bgcolor='#44CCCCCC',
        blur=ft.Blur(30, 15, ft.BlurTileMode.MIRROR),
        content=ft.Column(
            [
                content
            ],
            width=300,
            height=350,
        ),
        animate=ft.Animation(600, ft.AnimationCurve.DECELERATE),
    )
    main_column.controls = [
        tittle_bar,
    ]

    main_column.alignment = ft.MainAxisAlignment.CENTER

    page.update()
