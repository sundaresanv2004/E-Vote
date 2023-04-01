import flet as ft
import pandas as pd

from Main.authentication.scr.loc_file_scr import file_data
import Main.authentication.scr.election_scr as ee


def candidate_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Candidate"

    # Functions
    def page_resize(e):
        candidate_data_table.width = page.window_width - 150
        page.update()

    def add_candidate_page_fun(e):
        pass

    # Text & Buttons
    main_tittle_text = ft.Text(
        value="Records",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    add_candidate_button = ft.FloatingActionButton(
        icon=ft.icons.PERSON_ADD_ALT_1_ROUNDED,
        tooltip="Add new Candidate",
        on_click=add_candidate_page_fun,
    )

    # Read candidate data
    candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')

    # Table
    candidate_data_table = ft.DataTable(
        column_spacing=50,
        width=page.window_width - 150,
        columns=[
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Verification")),
            ft.DataColumn(ft.Text("Image")),
            ft.DataColumn(ft.Text(" "))
        ],
    )

    candidate_data_row: list = []
    if len(candidate_data_df) != 0:
        for i in range(len(candidate_data_df)):
            if candidate_data_df.loc[i].values[3] == True:
                verification_icon = ft.Icon(
                    name=ft.icons.DONE_ALL_ROUNDED,
                    color=ft.colors.GREEN_700,
                    size=30,
                )
            else:
                verification_icon = ft.Icon(
                    name=ft.icons.CLOSE_ROUNDED,
                    color=ft.colors.ERROR,
                    size=30,
                )
            if candidate_data_df.loc[i].values[5] != False:
                image_icon = ft.Icon(
                    name=ft.icons.DONE_ROUNDED,
                    color=ft.colors.GREEN_700,
                    size=30,
                )
            else:
                image_icon = ft.Icon(
                    name=ft.icons.CLOSE_ROUNDED,
                    color=ft.colors.ERROR,
                    size=30,
                )
            candidate_data_row.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(i + 1)),
                        ft.DataCell(ft.Text(f'{candidate_data_df.loc[i].values[2]}')),
                        ft.DataCell(ft.Text(f'{candidate_data_df.loc[i].values[3]}')),
                        ft.DataCell(verification_icon),
                        ft.DataCell(image_icon),
                        # ft.DataCell(ViewStaffRecord(page, content_column, i, title_text))
                    ],
                )
            )

    candidate_data_table.rows = candidate_data_row
    data_list1: list = [
        ft.Row(
            [
                candidate_data_table,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]

    if len(candidate_data_df) == 0:
        data_list1.append(
            ft.Row(
                [
                    ft.Text(
                        value="No Records",
                        size=20,
                    )
                ],
                height=page.window_height - 400,
                width=page.window_width - 100,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    row_1 = ft.Column(
        data_list1
    )
    candidate_home_column_data = ft.Column(
        expand=True,
        controls=[row_1],
        scroll=ft.ScrollMode.ADAPTIVE
    )

    content_column.controls = [
        ft.Row(
            [
                ft.Row(
                    [
                        main_tittle_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                ft.Row(
                    [
                        add_candidate_button,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Divider(
            height=5,
            thickness=3,
        ),
        candidate_home_column_data,
    ]

    page.on_resize = page_resize
    page.update()
