import flet as ft
import pandas as pd

from ..service.enc.encryption import decrypter
from ..service.scr.check_installation import path
from ..service.scr.loc_file_scr import file_path

column_1 = ft.Column()
main_column1 = None
search_entry = ft.TextField(
    hint_text="Search",
    hint_style=ft.TextStyle(color='f2f9f9', font_family='Verdana'),
    width=450,
    height=55,
    border=ft.InputBorder.OUTLINE,
    border_radius=50,
    disabled=True,
    focused_border_color='#f2f9f9',
    border_color='#ddeff0',
    prefix_style=ft.TextStyle(color=ft.colors.WHITE),
    text_style=ft.TextStyle(font_family='Verdana'),
    error_style=ft.TextStyle(font_family='Verdana'),
    prefix_icon=ft.icons.SEARCH_ROUNDED,
)


def staff_home_page(page: ft.Page, main_column: ft.Column):
    global search_entry, column_1, main_column1

    main_column1 = main_column

    def search(e):
        search_display_staff(page)

    search_entry.on_change = search

    main_column.controls = [
        ft.Container(
            margin=ft.margin.only(left=5, right=5),
            alignment=ft.alignment.center,
            content=search_entry,
        ),
        ft.Container(
            padding=5,
            content=column_1,
            expand=True,
        ),
    ]
    page.update()
    page.splash = None
    display_staff(page)


def search_display_staff(page: ft.Page):
    # file
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')
    name_enc = list(staff_df['name'].values)

    row_staff_data_list: list = []
    if len(search_entry.value) != 0:
        for i in name_enc:
            if search_entry.value.lower() in decrypter(i).lower():
                row_staff_data_list.append(ViewStaffRecord(page, main_column1, name_enc.index(i)))
        column_1.controls = row_staff_data_list
        page.update()
    else:
        display_staff(page)


def display_staff(page):
    global column_1
    # file
    staff_df = pd.read_json(path + file_path['admin_data'], orient='table')

    search_entry.value = None

    row_staff_data_list: list = []

    if len(staff_df) == 0:
        row_staff_data_list.append(
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
        for i in range(len(staff_df.index)):
            row_staff_data_list.append(ViewStaffRecord(page, main_column1, i))
        column_1.scroll = ft.ScrollMode.ADAPTIVE
        search_entry.disabled = False
        column_1.expand = True

    column_1.controls = row_staff_data_list
    page.update()


class ViewStaffRecord(ft.UserControl):

    def __init__(self, page, column, index_val):
        super().__init__()
        self.page = page
        self.column = column
        self.index_val = index_val
        self.staff_df = pd.read_json(path + file_path['admin_data'], orient='table')

    def edit(self, e):
        import Main.service.user.login_enc as cc
        from Main.pages.staff_edit import staff_edit_page
        from Main.functions.dialogs import message_dialogs
        if self.index_val == 0:
            if cc.teme_data[0] == 1:
                staff_edit_page(self.page, self.index_val, False)
            else:
                message_dialogs(self.page, "Edit this record?")
        else:
            staff_edit_page(self.page, self.index_val, False)

    def profile(self, e):
        from Main.pages.staff_profile import staff_profile_page
        staff_profile_page(self.page, self.staff_df.loc[self.index_val].values[0])

    def delete(self, e):
        from Main.functions.dialogs import message_dialogs
        from Main.pages.staff_delete import delete_staff_dialogs
        if self.index_val == 0:
            message_dialogs(self.page, "Delete this record?")
        else:
            delete_staff_dialogs(self.page, self.staff_df.loc[self.index_val].values[0], False)

    def build(self):
        self_icon = ft.CircleAvatar(
            content=ft.Icon(
                name=ft.icons.ACCOUNT_CIRCLE,
            ),
        )

        single_box_row = ft.Card(
            ft.Container(
                ft.ListTile(
                    leading=self_icon,
                    title=ft.Text(
                        value=f"{decrypter(self.staff_df.loc[self.index_val].values[1])}",
                        font_family='Verdana',
                    ),
                    subtitle=ft.Text(
                        value=f"{decrypter(self.staff_df.loc[self.index_val].values[2])}",
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
