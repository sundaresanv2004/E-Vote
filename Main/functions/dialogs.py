from time import sleep
import flet as ft

from Main.authentication.scr.loc_file_scr import message_data


def message_dialogs(page: ft.Page, message_key: str):
    # Functions
    def on_ok(e):
        message_alertdialog.open = False
        page.update()
        if message_key == "Restart Required":
            page.window_destroy()

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"{message_key}",
        ),
        content=ft.Text(
            value=f"{message_data[message_key]}",
        ),
        actions=[
            ft.TextButton(
                text="Ok",
                on_click=on_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()


def loading_dialogs(page: ft.Page, text: str, time_sleep: float):
    alertdialog = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value=f"{text}",
                            size=25,
                            weight="bold",
                            italic=True,
                        ),
                    ],
                    expand=True,
                    alignment='center',
                ),
                ft.Row(
                    [
                        ft.ProgressRing(),
                    ],
                    alignment='center',
                ),
            ],
            expand=True,
            alignment='center',
            spacing=8,
            height=180,
            width=100,
        )
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()

    sleep(time_sleep)

    alertdialog.open = False
    page.update()
