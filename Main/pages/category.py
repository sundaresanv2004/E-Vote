import flet as ft
import pandas as pd

from Main.authentication.scr.loc_file_scr import file_data
import Main.authentication.scr.election_scr as ee


def category_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Election > Category"

    # Functions
    def back_category(e):
        from .election_home import election_home_page
        content_column.clean()
        content_column.update()
        election_home_page(page, content_column, title_text)

    def page_resize(e):
        category_data_table.width = page.window_width - 150
        page.update()

    def add_category_page_fun(e):
        category_add_page(page, content_column, title_text, True)

    # Button
    back_category_home_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip="Back",
        on_click=back_category,
    )

    add_category_button = ft.FloatingActionButton(
        icon=ft.icons.ADD_ROUNDED,
        tooltip="Add new Category",
        on_click=add_category_page_fun,
    )

    # Read candidate data
    category_data_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')

    # Table
    category_data_table = ft.DataTable(
        column_spacing=50,
        width=page.window_width - 150,
        columns=[
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Qualification")),
            ft.DataColumn(ft.Text(""))
        ],
    )

    category_data_row: list = []
    if len(category_data_df) != 0:
        for i in range(len(category_data_df)):
            category_data_row.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(value=f"{i + 1}")),
                        ft.DataCell(ft.Text(value=f"{category_data_df.loc[i].values[1]}")),
                        ft.DataCell(ft.Text(value=f"{category_data_df.loc[i].values[2]}")),
                        ft.DataCell(ft.Text(value=f"{category_data_df.loc[i].values[2]}")),
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
                        back_category_home_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        ft.Text(
                            value="Records",
                            size=35,
                            weight=ft.FontWeight.BOLD,
                            italic=True,
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        add_category_button,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ]
        ),
        ft.Divider(
            thickness=3,
            height=5,
        ),
        candidate_home_column_data,
    ]

    page.on_resize = page_resize
    page.update()


def category_add_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text, home_page: bool):
    # Functions
    def on_close(e):
        add_category_alertdialog.open = False
        page.update()

    category_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')
    category_list = category_df['category'].values

    def add_new_category(e):
        if len(category_entry.value) != 0:
            if category_entry.value not in category_list:
                category_entry.error_text = None
                category_entry.update()
                if len(qualification_entry.value) != 0:
                    qualification_entry.error_text = None
                    qualification_entry.update()
                    from ..authentication.files.write_files import category_add_new
                    from ..functions.snack_bar import snack_bar1
                    category_add_new([category_entry.value.upper(), qualification_entry.value])
                    if home_page is True:
                        content_column.clean()
                        content_column.update()
                        category_home_page(page, content_column, title_text)
                    on_close(e)
                    snack_bar1(page, "Successfully Added")
                else:
                    qualification_entry.error_text = "Enter the Category"
                    qualification_entry.focus()
                    qualification_entry.update()
            else:
                category_entry.error_text = "It looks like this category has already been created."
                category_entry.focus()
                category_entry.update()
        else:
            category_entry.error_text = "Enter the Category"
            category_entry.focus()
            category_entry.update()

    def on_change_category(e):
        if category_entry.value in category_list:
            category_entry.error_text = "It looks like this category has already been created."
        else:
            category_entry.error_text = None
        category_entry.update()

    qualification_entry = ft.TextField(
        hint_text="Enter Qualification for above Category",
        width=420,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        border_color=ft.colors.SECONDARY,
        prefix_icon=ft.icons.SCHOOL_ROUNDED,
        on_submit=add_new_category,
    )

    category_entry = ft.TextField(
        hint_text="Enter the Category",
        width=420,
        border=ft.InputBorder.OUTLINE,
        autofocus=True,
        border_radius=9,
        capitalization=ft.TextCapitalization.CHARACTERS,
        border_color=ft.colors.SECONDARY,
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        on_submit=add_new_category,
        on_change=on_change_category,
    )

    content_column1 = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Add new Category",
                                weight=ft.FontWeight.BOLD,
                                size=25,
                            )
                        ],
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.CLOSE_ROUNDED,
                                tooltip="Close",
                                on_click=on_close,
                            )
                        ]
                    )
                ]
            ),
            ft.Row(
                [
                    ft.Column(
                        [
                            category_entry,
                            qualification_entry,
                        ],
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        height=220,
        width=450,
    )

    # AlertDialog data
    add_category_alertdialog = ft.AlertDialog(
        modal=True,
        content=content_column1,
        actions=[
            ft.TextButton(
                text="Add",
                on_click=add_new_category,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = add_category_alertdialog
    add_category_alertdialog.open = True
    page.update()
