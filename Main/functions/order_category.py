from time import sleep
import flet as ft
import pandas as pd

from Main.authentication.files.settings_write import final_list
from Main.authentication.scr.loc_file_scr import file_data
import Main.authentication.scr.election_scr as ee
from Main.functions.dialogs import loading_dialogs

list_category = []


class CategoryList(ft.UserControl):

    def __init__(self, val, list_data):
        super().__init__()
        self.text = ft.Text(size=20, value=None)
        self.val = val
        self.data = list_data

    def on_click(self, e):
        global list_category, class_list
        if e in list_category:
            list_category.remove(e)
            self.text.value = None
        else:
            list_category.append(e)
            self.text.value = list_category.index(e) + 1
        self.text.update()

    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Checkbox(label=self.data[self.val], on_change=lambda e: self.on_click(self.data[self.val])),
                    ft.Row(expand=True),
                    self.text,
                    ft.Row(width=2),
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            width=450,
            height=50,
            border_radius=5,
            padding=10,
        )


def order_category_option(page: ft.Page):
    candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')
    df1 = candidate_data_df[candidate_data_df.verification == True].sort_values(by='category')

    category_data = df1.category.unique()
    temp_category_data = []

    for i in range(len(category_data)):
        temp_category_data.append(CategoryList(i, category_data))

    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    def on_save(e):
        message_alertdialog.open = False
        page.update()
        final_list(list_category)
        sleep(0.1)
        loading_dialogs(page, "Loading...", 1)

    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Chose Category Order"),
        content=ft.Container(
            content=ft.Column(
                controls=temp_category_data,
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            height=300,
        ),
        actions=[
            ft.TextButton(
                text="Save",
                on_click=on_save,
            ),
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()
