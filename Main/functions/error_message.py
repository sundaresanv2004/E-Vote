from time import sleep

import flet as ft

from Main.functions.troubleshooting import election_data_missing


def error_message_dialogs(page: ft.Page, error_key: str):

    def on_ok(e):
        alertdialog.open = False
        page.update()
        sleep(0.2)
        election_data_missing(page)

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Error!",
            font_family='Verdana',
        ),
        content=ft.Text(
            value=f"{error_key}",
            font_family='Verdana',
        ),
        actions=[
            ft.TextButton(
                text="Ok",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()
