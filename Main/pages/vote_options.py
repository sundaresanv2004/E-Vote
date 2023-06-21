import flet as ft


def vote_exit(page: ft.Page):

    def on_no(e):
        exit_confirm_dialog.open = False
        page.update()

    def on_yes(e):
        exit_confirm_dialog.open = False
        page.update()
        page.clean()
        from main import main
        main(page)

    exit_confirm_dialog = ft.AlertDialog(
        modal=False,
        title=ft.Text("Confirm Exit"),
        content=ft.Text("Are you sure do you want to exit?", font_family='Verdana'),
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
    page.update()


def vote_done(page: ft.Page):

    def on_no(e):
        exit_confirm_dialog.open = False
        page.update()

    def on_yes(e):
        exit_confirm_dialog.open = False
        page.update()
        page.clean()
        from main import main
        main(page)

    exit_confirm_dialog = ft.AlertDialog(
        modal=False,
        title=ft.Text("Suc"),
        content=ft.Text("Are you sure do you want to exit?", font_family='Verdana'),
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
    page.update()
