from time import sleep
import flet as ft

from Main.authentication.scr.loc_file_scr import message_data, error_data


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
                            weight=ft.FontWeight.BOLD,
                            italic=True,
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ProgressRing(),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
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


def error_dialogs(page: ft.Page, error_key: str):

    def on_ok(e):
        alertdialog.open = False
        page.update()

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value=f"Error {error_key}!",
        ),
        content=ft.Text(
            value=f"{error_data[error_key]}",
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
