from time import sleep
import flet as ft
import pandas as pd

from Main.authentication.scr.check_installation import path
from Main.authentication.scr.loc_file_scr import file_path


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
                staff_edit_page(self.page, self.column, self.title_text, self.index_val)
            else:
                message_dialogs(self.page, "Edit this record?")
        else:
            self.column.clean()
            self.column.update()
            staff_edit_page(self.page, self.column, self.title_text, self.index_val)

    def profile(self, e):
        from Main.pages.staff_profile import staff_profile_page
        staff_profile_page(self.page, self.column, self.title_text, self.ad_df.loc[self.index_val].values[0])

    def delete(self, e):
        from Main.functions.dialogs import message_dialogs
        from Main.pages.staff_delete import delete_staff_dialogs
        if self.index_val == 0:
            message_dialogs(self.page, "Delete this record?")
        else:
            delete_staff_dialogs(self.page, self.column, self.ad_df.loc[self.index_val].values[0], self.title_text, False)

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
