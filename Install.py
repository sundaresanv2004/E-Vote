import subprocess
import platform
import os
import shutil
from time import sleep

command = 'pip install flet==0.7.4'
subprocess.run(command, shell=True)

import flet as ft


def main(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_skip_task_bar = True
    page.window_focused = True
    page.window_always_on_top = True
    page.window_frameless = True
    page.window_height = 300
    page.window_width = 500
    page.vertical_alignment = ft.alignment.center
    page.horizontal_alignment = ft.alignment.center
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()
    page.window_center()

    source = r".\3.01"
    destination = os.getenv('APPDATA') + r'\E-Vote\versions'

    if not os.path.exists(path):
        page.splash = ft.ProgressBar()
        column = ft.Column(
            [
                ft.Text(
                    value="Installing....",
                    weight=ft.FontWeight.W_500,
                    size=25,
                ),
                ft.ProgressRing(),
            ],
            height=300,
            width=500,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.update()
        page.add(column)
        sleep(10)
        command1 = 'pip install -r requirements.txt'
        subprocess.run(command1, shell=True)
        os.makedirs(path + r'\versions')
        shutil.move(source, destination)
        column.controls = [
            ft.Text(
                value="Successfully Installed",
                weight=ft.FontWeight.W_500,
                size=25,
            ),
            ft.ElevatedButton(
                text="Close",
                icon_color=ft.icons.CLOSE_ROUNDED,
                height=50,
                width=100,
                on_click=lambda e: page.window_destroy()
            )
        ]
        page.splash = None
        page.update()
    else:
        column = ft.Column(
            [
                ft.Text(
                    value="App Installed!",
                    weight=ft.FontWeight.W_500,
                    size=25,
                ),
                ft.ElevatedButton(
                    text="Delete App",
                    icon_color=ft.icons.CLOSE_ROUNDED,
                    height=50,
                    width=150,
                    on_click=lambda _: on_delete(page, column)
                ),
                ft.ElevatedButton(
                    text="Close",
                    icon_color=ft.icons.CLOSE_ROUNDED,
                    height=50,
                    width=150,
                    on_click=lambda e: page.window_destroy()
                )
            ],
            height=300,
            width=500,
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.add(column)


def on_delete(page: ft.Page, column: ft.Column):
    page.splash = ft.ProgressBar()
    column.controls = [
        ft.Text(
            value="Uninstalling....",
            weight=ft.FontWeight.W_500,
            size=25,
        ),
        ft.ProgressRing(),
    ]
    page.update()
    sleep(10)
    try:
        shutil.rmtree(path)
    except OSError:
        pass
    column.controls = [
        ft.Text(
            value="Successfully Uninstalled",
            weight=ft.FontWeight.W_500,
            size=25,
        ),
        ft.ElevatedButton(
            text="Close",
            icon_color=ft.icons.CLOSE_ROUNDED,
            height=50,
            width=100,
            on_click=lambda e: page.window_destroy()
        )
    ]
    page.splash = None
    page.update()


if __name__ == '__main__':

    if platform.system() == "Windows":
        os_sys = "Windows"
        path = os.getenv('APPDATA') + r'\E-Vote'

        ft.app(target=main)
    else:
        print("-----This app only supports on Windows-----")
        print("-----We are working on your os-----")
        exit()
