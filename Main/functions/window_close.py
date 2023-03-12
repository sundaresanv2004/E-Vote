import flet as ft


def close_true(page: ft.Page):

    def on_yes(e):
        page.window_destroy()

    def on_no(e):
        exit_confirm_dialog.open = False
        page.window_title_bar_hidden = False
        page.update()

    exit_confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Exit"),
        content=ft.Text("Are you sure do you want to exit?"),
        actions=[
            ft.TextButton(
                "Yes",
                on_click=on_yes,
            ),
            ft.TextButton(
                "No",
                on_click=on_no,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = exit_confirm_dialog
    exit_confirm_dialog.open = True
    page.window_title_bar_hidden = True
    page.update()
