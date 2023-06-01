import flet as ft
import pandas as pd

from ..authentication.scr.loc_file_scr import file_data
import Main.authentication.scr.election_scr as ee
from ..functions.dialogs import message_dialogs


def candidate_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Candidate"

    # Functions
    def page_resize(e):
        candidate_data_table.width = page.window_width - 150
        page.update()

    def add_candidate_page_fun(e):
        ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
        if not ele_ser.loc['lock_data'].values[0]:
            from .candidate_add import candidate_add_page
            content_column.clean()
            content_column.update()
            candidate_add_page(page, content_column, title_text)
        else:
            message_dialogs(page, "Data is Locked")

    # Text & Buttons
    main_title_text = ft.Text(
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
        column_spacing=10,
        width=page.window_width - 150,
        columns=[
            ft.DataColumn(ft.Text(value="#")),
            ft.DataColumn(ft.Text(value="Name")),
            ft.DataColumn(ft.Text(value="Category")),
            ft.DataColumn(ft.Text(value="Qualification")),
            ft.DataColumn(ft.Text(value="Verification")),
            ft.DataColumn(ft.Text(value="Added on")),
            ft.DataColumn(ft.Text(value="Image")),
            ft.DataColumn(ft.Text(value=" "))
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
                        ft.DataCell(ft.Text(value=f'{i + 1}')),
                        ft.DataCell(ft.Text(value=f'{candidate_data_df.loc[i].values[1]}')),
                        ft.DataCell(ft.Text(value=f'{candidate_data_df.loc[i].values[2]}')),
                        ft.DataCell(ft.Text(value=f'{candidate_data_df.loc[i].values[4]}')),
                        ft.DataCell(verification_icon),
                        ft.DataCell(ft.Text(value=f'{candidate_data_df.loc[i].values[6]}')),
                        ft.DataCell(image_icon),
                        ft.DataCell(ViewCandidateRecord(page, content_column, i, title_text))
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
                        main_title_text,
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


class ViewCandidateRecord(ft.UserControl):

    def __init__(self, page: ft.Page, content_column: ft.Column, index_val: int, title_text: ft.Text):
        super().__init__()
        self.option1 = None
        self.page = page
        self.content_column = content_column
        self.index_val = index_val
        self.title_text = title_text
        self.candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}',
                                              orient='table')
        self.ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')

    def edit(self, e):
        if not self.ele_ser.loc['lock_data'].values[0]:
            from .candidate_edit import candidate_edit_page
            self.content_column.clean()
            self.content_column.update()
            candidate_edit_page(self.page, self.content_column, self.title_text, self.index_val)
        else:
            message_dialogs(self.page, "Data is Locked")

    def delete(self, e):
        if not self.ele_ser.loc['lock_data'].values[0]:
            from .candidate_delete_approve import delete_candidate_dialogs
            delete_candidate_dialogs(self.page, self.content_column, self.index_val, self.title_text, False)
        else:
            message_dialogs(self.page, "Data is Locked")

    def profile(self, e):
        from .candidate_profile import candidate_profile_page
        candidate_profile_page(self.page, self.content_column, self.title_text, self.index_val)

    def verification(self, e):
        if not self.ele_ser.loc['lock_data'].values[0]:
            from .candidate_delete_approve import approve_dialogs
            approve_dialogs(self.page, self.content_column, self.title_text, self.index_val,
                            self.candidate_data_df.loc[self.index_val].values[3], False)
        else:
            message_dialogs(self.page, "Data is Locked")

    def build(self):
        if self.candidate_data_df.loc[self.index_val].values[3]:
            data = "Validated"
        else:
            data = "Validate"
        self.option1 = ft.PopupMenuItem(
            text=data,
            on_click=self.verification,
            checked=self.candidate_data_df.loc[self.index_val].values[3],
        )
        options = ft.PopupMenuButton(
            icon=ft.icons.MORE_VERT_ROUNDED,
            tooltip="Options",
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
                ft.PopupMenuItem(),
                self.option1
            ],
        )

        return options
