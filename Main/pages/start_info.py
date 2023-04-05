from time import sleep
import flet as ft

import Main.functions.theme as tt
from Main.functions.animations import menu_container_animation


def start_info_page(page: ft.Page, menu_container: ft.Container, input_data1: list):
    # Functions
    def back(e):
        back_button.disabled = True
        menu_container.clean()
        page.update()
        from Main.pages.menu import menu_page
        menu_container_animation(menu_container)
        sleep(0.1)
        menu_page(page, menu_container)

    def type_dropdown_change(e):
        progressbar_column.controls = [progressbar]
        type_dropdown.error_text = ''
        page.update()
        sleep(0.8)
        main_text.value = f"{e.data} Details"
        type_name_entry.hint_text = f"Enter the {e.data} name"
        progressbar_column.controls = []
        page.update()

    def check_entry_valid(e):
        if len(type_name_entry.value) != 0:
            type_name_entry.suffix_icon = None
            type_name_entry.error_text = None
        else:
            type_name_entry.error_text = "Enter the school/college name"
            type_name_entry.suffix_icon = ft.icons.ERROR_OUTLINE_ROUNDED
        type_name_entry.update()

    def on_back_data():
        if len(input_data1) != 0:
            type_dropdown.value = input_data1[0]
            type_name_entry.value = input_data1[1]
            main_text.value = f"{input_data1[0]} Details"
            type_name_entry.hint_text = f"Enter the {input_data1[0]} name"
            page.update()

    def next_button_click(e):
        check_entry_valid(e)

        if type_dropdown.value is not None:
            type_dropdown.error_text = ''
            type_dropdown.update()
            if len(type_name_entry.value) != 0:
                progressbar_column.controls = [progressbar]
                menu_container.disabled = True
                page.update()
                sleep(1)
                from Main.pages.admin_info import admin_info_page
                menu_container.clean()
                sleep(0.2)
                page.update()
                admin_info_page(page, menu_container, [type_dropdown.value, type_name_entry.value])
            else:
                progressbar_column.controls = None
                menu_container.disabled = False
                type_name_entry.focus()
                page.update()
        else:
            type_dropdown.error_text = 'Choose the type'
            type_dropdown.update()

    # Main title
    main_text = ft.Text(
        value="School/College Details",
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    # Buttons
    # back button
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip='Back',
        on_click=back,
    )

    # next button
    next_button = ft.ElevatedButton(
        text="Next",
        height=50,
        width=120,
        on_click=next_button_click,
    )

    # Input Fields
    type_dropdown = ft.Dropdown(
        hint_text="Choose the type",
        width=400,
        prefix_icon=ft.icons.SCHOOL_ROUNDED,
        border_color=ft.colors.SECONDARY,
        border_radius=9,
        on_change=type_dropdown_change,
        options=[
            ft.dropdown.Option("School"),
            ft.dropdown.Option("College"),
            ft.dropdown.Option("Other"),
        ]
    )

    type_name_entry = ft.TextField(
        hint_text="Enter the School/College name",
        width=400,
        capitalization=ft.TextCapitalization.CHARACTERS,
        filled=False,
        border_radius=9,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.colors.SECONDARY,
        on_change=check_entry_valid,
        on_submit=next_button_click,
    )

    # Progressbar
    progressbar = ft.ProgressBar(
        width=465,
        bgcolor=ft.colors.TRANSPARENT,
    )
    progressbar_column = ft.Column(
        height=10
    )

    # alignment and data
    menu_container.content = ft.Column(
        [
            progressbar_column,
            ft.Row(
                [
                    ft.Row(
                        [
                            back_button,
                        ],
                    ),
                    ft.Row(
                        [
                            main_text,
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            tt.ThemeIcon(page),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Column(
                height=35,
            ),
            ft.Column(
                [
                    type_dropdown,
                    type_name_entry,
                ],
                spacing=40
            ),
            ft.Column(
                height=30,
            ),
            ft.Row(
                [
                    next_button,
                ],
                width=400,
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Column(
                height=20,
            )
        ],
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    menu_container.padding = 0.3
    menu_container.update()
    on_back_data()
