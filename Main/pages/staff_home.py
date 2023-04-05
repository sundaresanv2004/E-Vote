import flet as ft
import pandas as pd

from Main.authentication.encrypter.encryption import decrypter
from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path
import Main.authentication.user.login_enc as cc


def staff_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Staff"

    # Functions
    def add_staff_page_fun(e):
        from Main.pages.staff_add import staff_add_page
        content_column.clean()
        content_column.update()
        staff_add_page(page, content_column, title_text)

    def page_resize(e):
        staff_data_table.width = page.window_width - 150
        page.update()

    # Text & Button
    main_title_text = ft.Text(
        value="Records",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    add_staff_button = ft.FloatingActionButton(
        icon=ft.icons.PERSON_ADD_ALT_1_ROUNDED,
        tooltip="Add new Staff",
        on_click=add_staff_page_fun,
    )

    # file
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')

    # Table
    staff_data_table = ft.DataTable(
        column_spacing=50,
        width=page.window_width - 150,
        columns=[
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Mail ID")),
            ft.DataColumn(ft.Text("Password")),
            ft.DataColumn(ft.Text("Permission")),
            ft.DataColumn(ft.Text(" "))
        ],
    )

    staff_data_row: list = []
    if len(staff_df) != 0:
        for i in range(len(staff_df)):
            if staff_df.loc[i].values[4] == True:
                permission = ft.Icon(
                    name=ft.icons.DONE_ALL_ROUNDED,
                    color=ft.colors.GREEN_700,
                    size=30,
                )
            else:
                permission = ft.Icon(
                    name=ft.icons.CLOSE_ROUNDED,
                    color=ft.colors.ERROR,
                    size=30,
                )
            if cc.teme_data[0] != 1:
                if i == 0:
                    password_text = ft.Text(f'*' * len(decrypter(staff_df.loc[i].values[3])))
                else:
                    password_text = ft.Text(f'{decrypter(staff_df.loc[i].values[3])}')
            else:
                password_text = ft.Text(f'{decrypter(staff_df.loc[i].values[3])}')

            staff_data_row.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(value=f"{i + 1}")),
                        ft.DataCell(ft.Text(f'{decrypter(staff_df.loc[i].values[1])}')),
                        ft.DataCell(ft.Text(f'{decrypter(staff_df.loc[i].values[2])}')),
                        ft.DataCell(password_text),
                        ft.DataCell(permission),
                        ft.DataCell(ViewStaffRecord(page, content_column, i, title_text))
                    ],
                )
            )

    staff_data_table.rows = staff_data_row
    data_list1: list = [
        ft.Row(
            [
                staff_data_table,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]

    if len(staff_df) == 0:
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
    staff_home_column_data = ft.Column(
        expand=True,
        controls=[row_1],
        scroll=ft.ScrollMode.ADAPTIVE
    )

    content_column.controls = [
        ft.Row(
            [
                ft.Row(
                    [
                        main_title_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                ft.Row(
                    [
                        add_staff_button,
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
        staff_home_column_data,
    ]

    page.on_resize = page_resize
    page.update()


class ViewStaffRecord(ft.UserControl):

    def __init__(self, page, column, index_val, title):
        super().__init__()
        self.page = page
        self.column = column
        self.index_val = index_val
        self.title_text = title
        self.ad_df = pd.read_json(path + file_path['admin_data'], orient='table')

    def edit(self, e):
        import Main.authentication.user.login_enc as cc
        from Main.pages.staff_edit import staff_edit_page
        from Main.functions.dialogs import message_dialogs
        if self.index_val == 0:
            if cc.teme_data[0] == 1:
                self.column.clean()
                self.column.update()
                staff_edit_page(self.page, self.column, self.title_text, self.index_val, False)
            else:
                message_dialogs(self.page, "Edit this record?")
        else:
            self.column.clean()
            self.column.update()
            staff_edit_page(self.page, self.column, self.title_text, self.index_val, False)

    def profile(self, e):
        from Main.pages.staff_profile import staff_profile_page
        staff_profile_page(self.page, self.column, self.title_text, self.ad_df.loc[self.index_val].values[0])

    def delete(self, e):
        from Main.functions.dialogs import message_dialogs
        from Main.pages.staff_delete import delete_staff_dialogs
        if self.index_val == 0:
            message_dialogs(self.page, "Delete this record?")
        else:
            delete_staff_dialogs(self.page, self.column, self.ad_df.loc[self.index_val].values[0], self.title_text,
                                 False)

    def build(self):
        return ft.PopupMenuButton(
            tooltip="Options",
            icon=ft.icons.MORE_VERT_ROUNDED,
            items=[
                ft.PopupMenuItem(
                    text="View Profile",
                    icon=ft.icons.STREETVIEW_ROUNDED,
                    on_click=self.profile
                ),
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
