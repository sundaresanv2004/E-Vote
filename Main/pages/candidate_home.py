import flet as ft
import pandas as pd

from ..functions.dialogs import message_dialogs
from ..service.scr.loc_file_scr import file_data
import Main.service.scr.election_scr as ee

column_1 = ft.Column()
main_column1 = None
search_entry = ft.TextField(
    hint_text="Search",
    hint_style=ft.TextStyle(color='f2f9f9', font_family='Verdana'),
    width=450,
    border=ft.InputBorder.OUTLINE,
    height=55,
    disabled=True,
    border_radius=50,
    focused_border_color='#f2f9f9',
    border_color='#ddeff0',
    prefix_style=ft.TextStyle(color=ft.colors.WHITE),
    text_style=ft.TextStyle(font_family='Verdana'),
    prefix_icon=ft.icons.SEARCH_ROUNDED,
)


def candidate_home_page(page: ft.Page, main_column: ft.Column):
    global search_entry, column_1, main_column1

    main_column1 = main_column

    def search(e):
        search_display_candidate(page)

    search_entry.on_change = search
    search_entry.value = None

    main_column.controls = [
        ft.Container(
            margin=ft.margin.only(left=5, right=5),
            content=search_entry,
            alignment=ft.alignment.center,
        ),
        ft.Container(
            padding=5,
            content=column_1,
            expand=True,
        ),
    ]
    page.update()
    page.splash = None
    display_candidate(page)


def search_display_candidate(page: ft.Page):
    # file
    candidate_data_df = pd.read_json(ee.current_election_path + rf'/{file_data["candidate_data"]}', orient='table')
    name_enc = list(candidate_data_df['candidate_name'].values)
    cat_enc = list(candidate_data_df['category'].unique())

    row_can_data_list: list = []
    data_in: list = []
    if len(search_entry.value) != 0:
        for i in name_enc:
            if search_entry.value.lower() in i.lower():
                if name_enc.index(i) not in data_in:
                    row_can_data_list.append(ViewStaffRecord(page, main_column1, name_enc.index(i)))
                    data_in.append(name_enc.index(i))

        for j in cat_enc:
            if search_entry.value.lower() in j.lower():
                for k in list(candidate_data_df[candidate_data_df.category == j].index.values):
                    if k not in data_in:
                        row_can_data_list.append(ViewStaffRecord(page, main_column1, k))
                        data_in.append(k)

        column_1.controls = row_can_data_list
        page.update()
    else:
        display_candidate(page)


def display_candidate(page):
    global column_1
    # file
    candidate_data_df = pd.read_json(ee.current_election_path + rf'/{file_data["candidate_data"]}', orient='table')

    row_can_data_list = []

    if len(candidate_data_df) == 0:
        row_can_data_list.append(
            ft.Row(
                [
                    ft.Text(
                        value="No record found",
                        size=25,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        column_1.alignment = ft.MainAxisAlignment.CENTER
    else:
        for i in range(len(candidate_data_df.index)):
            row_can_data_list.append(ViewStaffRecord(page, main_column1, i))
        column_1.expand = True
        search_entry.disabled = False
        column_1.scroll = ft.ScrollMode.ADAPTIVE

    column_1.controls = row_can_data_list
    page.update()


class ViewStaffRecord(ft.UserControl):

    def __init__(self, page, column, index_val):
        super().__init__()
        self.page = page
        self.index_val = index_val
        self.column = column
        self.candidate_data_df = pd.read_json(ee.current_election_path + rf'/{file_data["candidate_data"]}',
                                              orient='table')
        self.ele_ser = pd.read_json(ee.current_election_path + fr"/{file_data['election_settings']}", orient='table')
        self.candidate_image_destination = ee.current_election_path + r'/images'

    def edit(self, e):
        if not self.ele_ser.loc['lock_data'].values[0]:
            from .candidate_edit import candidate_edit_page
            candidate_edit_page(self.page, self.index_val, False)
        else:
            message_dialogs(self.page, "Option is locked")

    def profile(self, e):
        from .candidate_profile import candidate_profile_page
        candidate_profile_page(self.page, self.index_val)

    def delete(self, e):
        if not self.ele_ser.loc['lock_data'].values[0]:
            from .candidate_delete import delete_candidate_dialogs
            delete_candidate_dialogs(self.page, self.index_val, False)
        else:
            message_dialogs(self.page, "Option is locked")

    def build(self):
        if not self.candidate_data_df.loc[self.index_val].values[5]:
            self_icon = ft.CircleAvatar(
                content=ft.Icon(
                    name=ft.icons.ACCOUNT_CIRCLE,
                ),
            )
        else:
            self_icon = ft.Container(
                width=50,
                height=50,
                alignment=ft.alignment.center,
                border_radius=50,
                image_src=self.candidate_image_destination + rf'/{self.candidate_data_df.loc[self.index_val].values[5]}',
                image_fit=ft.ImageFit.COVER
            )

        single_box_row = ft.Card(
            ft.Container(
                ft.ListTile(
                    leading=self_icon,
                    title=ft.Text(
                        value=f"{self.candidate_data_df.loc[self.index_val].values[1]}",
                        font_family='Verdana',
                    ),
                    subtitle=ft.Text(
                        value=f"{self.candidate_data_df.loc[self.index_val].values[2]}",
                        font_family='Verdana',
                    ),
                    trailing=ft.PopupMenuButton(
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
                    ),
                    on_click=self.profile,
                ),
                padding=ft.padding.symmetric(vertical=3.5),
                blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
                border_radius=10,
            ),
            elevation=0,
            color=ft.colors.with_opacity(0.4, '#44CCCCCC')
        )

        return single_box_row
