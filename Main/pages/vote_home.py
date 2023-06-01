import flet as ft
import pandas as pd

from ..authentication.scr.check_installation import path
from ..authentication.scr.loc_file_scr import file_path


def vote_page(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def logout_fun(e):
        logout(page)

    app_data_df = pd.read_json(path + file_path['app_data'], orient='table')

    page_title_text = ft.Text(
        value=app_data_df[app_data_df.topic == 'institution_name'].values[0][1],
        size=35,
        weight=ft.FontWeight.BOLD,
    )
    log_out = ft.IconButton(
        icon=ft.icons.LOGOUT_ROUNDED,
        icon_size=25,
        tooltip="Logout",
        on_click=logout_fun
    )

    # AppBar
    appbar = ft.AppBar(
        title=page_title_text,
        leading_width=50,
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[log_out],
    )

    page.add(appbar)


def logout(page: ft.Page):
    # Functions
    def on_ok(e):
        on_cancel(e)
        page.clean()
        page.update()
        import main
        main.main(page)

    def on_cancel(e):
        message_alertdialog.open = False
        page.update()

    # AlertDialog data
    message_alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(value="Make Sure?"),
        content=ft.Text(value="Are you sure do you want to logout?"),
        actions=[
            ft.TextButton(
                text="Yes",
                on_click=on_ok,
            ),
            ft.TextButton(
                text="No",
                on_click=on_cancel,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Open dialog
    page.dialog = message_alertdialog
    message_alertdialog.open = True
    page.update()
