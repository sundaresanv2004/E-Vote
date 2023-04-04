from time import sleep
import flet as ft

from Main.functions.dialogs import loading_dialogs


def delete_staff_dialogs(page: ft.Page, content_column: ft.Column, index_df, title_text, view):
    # Functions
    def del_ok(e):
        from Main.pages.staff_home import staff_home_page
        from Main.authentication.files.write_files import delete_staff_data
        from Main.functions.snack_bar import snack_bar1
        import Main.authentication.user.login_enc as cc
        delete_staff_data(index_df)
        alertdialog.open = False
        page.update()
        sleep(0.2)
        loading_dialogs(page, "Deleting...", 2)
        sleep(0.1)
        content_column.clean()
        content_column.update()
        snack_bar1(page, "Successfully Deleted.")
        staff_home_page(page, content_column, title_text)
        sleep(0.5)
        if cc.teme_data[0] == index_df:
            page.splash = ft.ProgressBar()
            page.update()
            from main import main
            loading_dialogs(page, "Logging out...", 7)
            sleep(0.5)
            page.splash = None
            page.update()
            page.clean()
            main(page)

    def on_close(e):
        alertdialog.open = False
        page.update()
        if view is True:
            sleep(0.2)
            from Main.pages.staff_profile import staff_profile_page
            staff_profile_page(page, content_column, title_text, index_df)

    # AlertDialog
    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Delete this record?",
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                on_click=on_close,
            ),
            ft.TextButton(
                text="Ok",
                on_click=del_ok,
            ),
        ],
        content=ft.Text(
            value="This record will be deleted forever.",
        ),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()
