import flet as ft
import pandas as pd
from time import sleep

from Main.service.scr.loc_file_scr import file_data
import Main.service.scr.election_scr as ee


def category_dialogs(page: ft.Page):
    category_dialogs1 = ft.AlertDialog(
        modal=True,
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def on_close(e):
        category_dialogs1.open = False
        page.update()

    def add_cat(e):
        category_dialogs1.open = False
        page.update()
        sleep(0.2)
        category_add_page(page, 'category')

    # Read category data
    category_data_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')

    # Table
    category_data_table = ft.DataTable(
        column_spacing=20,
        expand=True,
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
                        ft.DataCell(CategoryView(page, i, category_dialogs1))
                    ],
                )
            )

    category_data_table.rows = category_data_row
    data_list1: list = [
        ft.Row(
            [
                category_data_table,
            ],
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
                width=700,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    # AlertDialog data
    category_dialogs1.content = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Category",
                                weight=ft.FontWeight.BOLD,
                                size=25,
                                font_family='Verdana',
                            ),
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
                ],
                width=680,
            ),
            ft.Column(
                controls=data_list1,
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        height=450,
        width=700,
    )

    category_dialogs1.actions = [
        ft.TextButton(
            text="Add new category",
            on_click=add_cat,
        )
    ]

    # Open dialog
    page.dialog = category_dialogs1
    category_dialogs1.open = True
    page.update()


class CategoryView(ft.UserControl):
    def __init__(self, page: ft.Page, index_val, dialogs: ft.AlertDialog):
        super().__init__()
        self.page = page
        self.index_val = index_val
        self.dialogs = dialogs
        self.category_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')

    def edit(self, e):
        self.dialogs.open = False
        self.page.update()
        sleep(0.2)

        def on_close(e):
            add_category_alertdialog.open = False
            self.page.update()
            sleep(0.2)
            category_dialogs(self.page)

        def edit_category(e):
            if len(category_entry.value) != 0:
                category_entry.error_text = None
                category_entry.update()
                if len(qualification_entry.value) != 0:
                    qualification_entry.error_text = None
                    qualification_entry.update()
                    from ..service.files.write_files import category_edit
                    from ..functions.snack_bar import snack_bar1
                    category_edit([category_entry.value.upper(), qualification_entry.value], self.index_val)
                    on_close(e)
                    snack_bar1(self.page, "Successfully Updated")
                else:
                    qualification_entry.error_text = "Enter the Category"
                    qualification_entry.focus()
                    qualification_entry.update()
            else:
                category_entry.error_text = "Enter the Category"
                category_entry.focus()
                category_entry.update()

        qualification_entry = ft.TextField(
            hint_text="Enter Qualification for above Category",
            width=420,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            border_color=ft.colors.SECONDARY,
            prefix_icon=ft.icons.SCHOOL_ROUNDED,
            on_submit=edit_category,
            value=self.category_df.loc[self.index_val].values[2]
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
            on_submit=edit_category,
            value=self.category_df.loc[self.index_val].values[1]
        )

        content_column1 = ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    value="Edit Category",
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
                    text="Save",
                    on_click=edit_category,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Open dialog
        self.page.dialog = add_category_alertdialog
        add_category_alertdialog.open = True
        self.page.update()

    def delete(self, e):
        self.dialogs.open = False
        self.page.update()
        sleep(0.2)

        def del_ok(e):
            alert_delete_cat.open = False
            self.page.update()
            from ..service.files.write_files import delete_category
            from ..functions.snack_bar import snack_bar1
            delete_category(self.index_val)
            on_close(e)
            snack_bar1(self.page, "Successfully Deleted")

        def on_close(e):
            alert_delete_cat.open = False
            self.page.update()
            sleep(0.2)
            category_dialogs(self.page)

        # AlertDialog
        alert_delete_cat = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value="Delete this Category?",
            ),
            actions=[
                ft.TextButton(
                    text="Ok",
                    on_click=del_ok,
                ),
                ft.TextButton(
                    text="Cancel",
                    on_click=on_close,
                ),
            ],
            content=ft.Text(
                value="This Category will be deleted forever.",
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = alert_delete_cat
        alert_delete_cat.open = True
        self.page.update()

    def build(self):
        return ft.PopupMenuButton(
            tooltip="Options",
            icon=ft.icons.MORE_VERT_ROUNDED,
            items=[
                ft.PopupMenuItem(
                    text="Edit",
                    icon=ft.icons.EDIT_ROUNDED,
                    on_click=self.edit
                ),
                ft.PopupMenuItem(
                    text="Delete",
                    icon=ft.icons.DELETE_ROUNDED,
                    on_click=self.delete
                ),
            ],
        )


def category_add_page(page: ft.Page, page_view):
    # Functions
    def on_close(e):
        add_category_alertdialog.open = False
        page.update()
        sleep(0.2)
        if page_view == 'category':
            category_dialogs(page)
        elif page_view == 'candidate':
            from Main.pages.candidate_add import candidate_add_page
            candidate_add_page(page)

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
                    from ..service.files.write_files import category_add_new
                    from ..functions.snack_bar import snack_bar1
                    category_add_new([category_entry.value.upper(), qualification_entry.value])
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
