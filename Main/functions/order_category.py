from time import sleep
import flet as ft
import pandas as pd

from Main.functions.download_nomination import download_nomination
from Main.service.files.vote_settings_write import final_list
from Main.service.scr.loc_file_scr import file_data
import Main.service.scr.election_scr as ee
from Main.functions.dialogs import loading_dialogs

list_category = []


class CategoryList(ft.UserControl):

    def __init__(self, val):
        super().__init__()
        self.text = ft.Text(size=20, value=None)
        self.val = val

    def on_click_cat(self, e):
        global list_category
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
                    ft.Checkbox(
                        label=self.val,
                        data=self.val,
                        on_change=lambda e: self.on_click_cat(e.control.data)),
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

    def on_reset(e):
        global list_category
        message_alertdialog.open = False
        page.update()
        sleep(0.2)
        list_category = []
        order_category_option(page)

    temp_category_data = []
    if df1.empty is False:
        for i in list(df1.category.unique()):
            temp_category_data.append(CategoryList(i))
    else:
        temp_category_data.append(
            ft.Row(
                [
                    ft.Text(
                        value="No Records",
                        size=25,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=350,
                height=200,
            )
        )

    def on_ok(e):
        global list_category
        message_alertdialog.open = False
        page.update()
        list_category = []

    def on_save(e):
        message_alertdialog.open = False
        page.update()
        final_list(list_category)
        sleep(0.2)
        loading_dialogs(page, "Saving...", 1)
        sleep(0.2)
        download_nomination(page)

    save_button = ft.TextButton(
        text="Save",
        on_click=on_save,
    )

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
                text="Reset",
                on_click=on_reset,
            ),
            save_button,
            ft.TextButton(
                text="Cancel",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    if df1.empty:
        save_button.disabled = True

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()
