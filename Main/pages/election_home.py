import flet as ft


def election_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Election"

    # Text & Buttons
    main_title_text = ft.Text(
        value="Election",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    content_column.controls = [
        ft.Row(
            [
                ft.Row(
                    [
                        main_title_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Divider(
            height=5,
            thickness=3,
        ),
        # staff_home_column_data,
    ]

    page.update()
