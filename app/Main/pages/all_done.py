import flet as ft

import Main.functions.theme as tt


def all_done_page(page: ft.Page, menu_container: ft.Container):
    # Functions
    def submit_on_clicked(e):
        from Main.functions.dialogs import message_dialogs
        message_dialogs(page, 'Restart Required')

    def on_change_button(e):
        if checkbox_terms.value is True:
            submit_button.disabled = False
        else:
            submit_button.disabled = True
        submit_button.update()

    # Buttons
    # submit button
    submit_button = ft.ElevatedButton(
        text="Done",
        height=50,
        width=120,
        disabled=True,
        on_click=submit_on_clicked,
    )

    # Input Filed
    checkbox_terms = ft.Checkbox(
        label="I have read and understand the above information",
        value=False,
        on_change=on_change_button,
    )

    # alignment and data
    all_done_data_column = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                name=ft.icons.DONE_ROUNDED,
                                size=40,
                            ),
                            ft.Text(
                                value="All Done",
                                size=40,
                                weight=ft.FontWeight.BOLD,
                            ),
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
                height=10,
            ),
            ft.Column(
                [
                    ft.Text(
                        "aa\naaaa\naaaa\naaaaa\naaaaa\naaaaa\naaaa\naa\naaaa\naaaaa"
                    )
                ],
            ),
            ft.Column(
                height=20,
            ),
            ft.Row(
                [
                    checkbox_terms,
                ],
                width=680,
            ),
            ft.Row(
                [
                    submit_button,
                ],
                width=650,
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Column(
                height=40,
            ),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.ADAPTIVE,
    )

    menu_container.content = all_done_data_column
    menu_container.padding = 10
    menu_container.disabled = False
    menu_container.update()
