import flet as ft


class CandidateHomePage(ft.UserControl):

    def __init__(self, page: ft.Page, content_column: ft.Column):
        super().__init__()
        self.qualification_dropdown = None
        self.name_entry = None
        self.category_dropdown = None
        self.upload_button = None
        self.save_button = None
        self.main_column = None

        self.container = ft.Container(
            content=ft.Text("Upload Image"),
            width=200,
            height=250,
            alignment=ft.alignment.center,
            border=ft.border.all(0.5, ft.colors.SECONDARY),
            border_radius=ft.border_radius.all(5),
        )

    def build(self):
        self.save_button = ft.ElevatedButton(
            text="Save",
            height=50,
            width=150,
            disabled=True,
            # on_click=save_candidate,
        )

        self.upload_button = ft.TextButton(
            text="Upload Image",
            icon=ft.icons.FILE_UPLOAD_ROUNDED,
            # on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True, file_type=ft.FilePickerFileType.IMAGE),
        )

        self.name_entry = ft.TextField(
            # label="Enter the Candidate name",
            hint_text="Enter the Candidate name",
            width=450,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            border_color=ft.colors.SECONDARY,
            autofocus=True,
            prefix_icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
            # on_change=on_change_button,
            # on_submit=save_candidate,
        )

        self.qualification_dropdown = ft.Dropdown(
            # label="Choose Candidate Qualification",
            hint_text="Choose Candidate Qualification",
            width=450,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            # on_change=qualification_change,
            prefix_icon=ft.icons.CATEGORY_ROUNDED,
            border_color=ft.colors.SECONDARY,
        )

        self.category_dropdown = ft.Dropdown(
            # label="Choose Candidate Category",
            hint_text="Choose Candidate Category",
            width=450,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            options=[
                ft.dropdown.Option("Select Candidate Qualification"),
            ],
            prefix_icon=ft.icons.CATEGORY_ROUNDED,
            border_color=ft.colors.SECONDARY,
        )

        self.main_column = ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [

                                ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                self.container,
                                                self.upload_button,
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        ft.Column(
                                            [
                                                self.name_entry,
                                                self.qualification_dropdown,
                                                self.category_dropdown,
                                            ],
                                            spacing=40,
                                        )
                                    ],
                                    height=300,
                                    spacing=50,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    [
                                        self.save_button,
                                    ],
                                    width=720,
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                                ft.Row(
                                    height=5,
                                )

                            ],
                        ),
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            ],
            width=800,
            spacing=30,
        )

        return self.main_column


def candidate_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    def back_candidate_add_page(e):
        from .candidate_home import candidate_home_page
        content_column.clean()
        content_column.update()
        candidate_home_page(page, content_column, title_text)
    def can(e):
        from .category_home import category_home_page
        content_column.clean()
        content_column.update()
        category_home_page(page, content_column, title_text)

    title_text.value = "Candidate > Add Candidate"

    # Main Text
    main_staff_add_text = ft.Text(
        value="Add Candidate",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    # Button
    back_staff_home_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip="Back",
        on_click=back_candidate_add_page,
    )

    question_button = ft.PopupMenuButton(
        icon=ft.icons.QUESTION_ANSWER_ROUNDED,
        tooltip="Questions?",
        items=[
            ft.PopupMenuItem(
                icon=ft.icons.ADD_ROUNDED,
                text="Add new Category",
                on_click=can
            ),
        ]
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
                ft.Row(
                    [
                        question_button,
                    ],
                    alignment=ft.MainAxisAlignment.END,
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
                CandidateHomePage(page, content_column),
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
