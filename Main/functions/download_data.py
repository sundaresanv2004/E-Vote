import flet as ft
import pandas as pd
import os

import Main.authentication.scr.election_scr as ee
from ..authentication.scr.loc_file_scr import file_data


def download_nomination(page):
    def save_file_result(e: ft.FilePickerResultEvent):
        message_alertdialog.open = False
        page.update()
        path1 = e.path if e.path else False
        path_download = path1 + ".csv"
        if path_download is not False:
            candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["final_nomination"]}',
                                             orient='table')
            new_df = candidate_data_df[['candidate_name', 'category', 'qualification']]
            try:
                new_df.to_csv(path_download, index=False)
            except PermissionError:
                pass
            os.system(path_download)

    save_file_dialog = ft.FilePicker(on_result=save_file_result)

    def on_ok(e):
        message_alertdialog.open = False
        page.update()

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=False,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Download Nomination List", size=23),
                                ft.IconButton(
                                    icon=ft.icons.CLOSE_ROUNDED,
                                    icon_size=30,
                                    tooltip="Close",
                                    on_click=on_ok,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            [
                                ft.FloatingActionButton(
                                    icon=ft.icons.FILE_DOWNLOAD_ROUNDED,
                                    tooltip='Download',
                                    on_click=lambda _: save_file_dialog.save_file(file_name="Nomination_List",
                                                                                  file_type=ft.FilePickerFileType.ANY),
                                    disabled=page.web,
                                )
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    expand=True,
                )
            ],
            width=350,
            height=120,
        )
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()
    page.add(save_file_dialog)
