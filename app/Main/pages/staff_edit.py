import flet as ft


def staff_edit_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text, index_df):
    title_text.value = "Staff > Edit Staff"

    # Functions
    def back_staff_edit_page(e):
        from Main.pages.staff_home import staff_home_page
        content_column.clean()
        content_column.update()
        staff_home_page(page, content_column, title_text)

    # Main Text
    main_staff_add_text = ft.Text(
        value="Edit Staff",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    # Button
    back_staff_home_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip="Back",
        on_click=back_staff_edit_page,
    )

    content_column.controls = [
        ft.Row(
            [
                ft.Row(
                    [
                        back_staff_home_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    [
                        main_staff_add_text,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        ),
        ft.Divider(
            thickness=3,
            height=5,
        ),
        ft.Column(
            [
                ft.Row(
                    height=40,
                ),
                # add_staff_column_data,
                ft.Row(
                    height=10,
                )
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    ]

    page.update()
