import flet as ft
import pandas as pd

from Main.authentication.scr.loc_file_scr import file_data
import Main.authentication.scr.election_scr as ee


def category_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Category"

    # Functions
    def page_resize(e):
        category_data_table.width = page.window_width - 150
        page.update()

    def add_candidate_page_fun(e):
        from .candidate_add import candidate_home_page
        content_column.clean()
        content_column.update()
        candidate_home_page(page, content_column, title_text)

    # Text & Buttons
    main_tittle_text = ft.Text(
        value="Records",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    add_candidate_button = ft.FloatingActionButton(
        icon=ft.icons.ADD_ROUNDED,
        tooltip="Add new Category",
        on_click=add_candidate_page_fun,
    )

    # Read candidate data
    category_data_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')
    print(category_data_df)

    # Table
    category_data_table = ft.DataTable(
        column_spacing=50,
        width=page.window_width - 150,
        columns=[
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Qualification")),
            ft.DataColumn(ft.Text("No.of Records")),
            ft.DataColumn(ft.Text(""))
        ],
    )

    category_data_row: list = []
    if len(category_data_df) != 0:
        for i in range(len(category_data_df)):
            category_data_row.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(i + 1)),
                        ft.DataCell(ft.Text()),
                        ft.DataCell(ft.Text()),
                        ft.DataCell(ft.Text()),
                        # ft.DataCell(ViewStaffRecord(page, content_column, i, title_text))
                    ],
                )
            )

    category_data_table.rows = category_data_row
    data_list1: list = [
        ft.Row(
            [
                category_data_table,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]

    if len(category_data_df) == 0:
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
