import os
from time import sleep

import flet as ft
import pandas as pd

from Main.authentication.scr.loc_file_scr import file_data
import Main.authentication.scr.election_scr as ee


class CandidateHomePage:

    def __init__(self, page: ft.Page, content_column: ft.Column, title_text: ft.Text):
        super().__init__()
        self.page = page
        self.content_column = content_column
        self.title_text = title_text
        self.candidate_selected_image_name = False
        self.candidate_selected_file_path = None
        self.candidate_image_destination = ee.current_election_path + r'\images'

        # Input Fields
        self.name_entry = ft.TextField(
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
            hint_text="Choose Candidate Qualification",
            width=450,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            # on_change=qualification_change,
            prefix_icon=ft.icons.CATEGORY_ROUNDED,
            border_color=ft.colors.SECONDARY,
        )

        self.category_dropdown = ft.Dropdown(
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

        self.upload_button = None
        self.save_button = None
        self.main_column = None
        self.category_df = pd.read_csv(ee.current_election_path + rf'\{file_data["category_data"]}')
        self.container = ft.Container(
            content=ft.Text("Upload Image"),
            width=200,
            height=250,
            alignment=ft.alignment.center,
            border=ft.border.all(0.5, ft.colors.SECONDARY),
            border_radius=ft.border_radius.all(5),
        )

    def qualification_dropdown_values(self):
        option_list1: list = []
        temp_list: list = []

        if self.category_df.empty is not True:
            for i in range(len(self.category_df)):
                if self.category_df.loc[i].values[2] not in temp_list:
                    option_list1.append(ft.dropdown.Option(self.category_df.loc[i].values[2]))
                    temp_list.append(self.category_df.loc[i].values[2])
        else:
            option_list1.append(ft.dropdown.Option("No Category Records"))

        self.qualification_dropdown.options = option_list1

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        from ..functions.dialogs import error_dialogs
        if self.candidate_selected_image_name is not False:
            try:
                os.replace(self.candidate_image_destination, self.candidate_selected_file_path)
            except FileNotFoundError:
                pass

        self.candidate_selected_image_name = ", ".join(map(lambda f: f.name, e.files)) if e.files else False
        self.candidate_selected_file_path = ", ".join(map(lambda f: f.path, e.files)) if e.files else False

        if self.candidate_selected_image_name is not False:
            self.candidate_image_destination += rf'\{self.candidate_selected_image_name}'

            try:
                if not os.path.exists(self.candidate_image_destination):
                    os.replace(self.candidate_selected_file_path, self.candidate_image_destination)
                    self.container.content = ft.Text()
                    self.container.update()
                    self.container.image_src = self.candidate_image_destination
                    self.container.image_fit = ft.ImageFit.COVER
                    self.container.update()
                else:
                    error_dialogs(self.page, "001")
            except OSError:
                self.container.content = ft.Text("Upload Image")
                self.container.update()
                self.candidate_selected_image_name, self.candidate_selected_file_path = False, None
                self.candidate_image_destination = ee.current_election_path + r'\images'
                error_dialogs(self.page, "002")
        else:
            self.container.image_src = None
            self.container.content = ft.Text("Upload canceled!")
            self.container.update()

    def change_values(self):
        if self.candidate_selected_image_name is not False:
            try:
                os.replace(self.candidate_image_destination, self.candidate_selected_file_path)
            except FileNotFoundError:
                pass
        self.candidate_selected_image_name, self.candidate_selected_file_path = False, None
        self.candidate_image_destination = ee.current_election_path + r'\images'

    def back_candidate_home(self):
        from .candidate_home import candidate_home_page
        if len(self.name_entry.value) != 0:
            self.unsaved_dialogs()
        elif self.candidate_selected_image_name is not False:
            self.unsaved_dialogs()
        else:
            self.content_column.clean()
            self.content_column.update()
            candidate_home_page(self.page, self.content_column, self.title_text)

    def build(self):
        self.save_button = ft.ElevatedButton(
            text="Save",
            height=50,
            width=150,
            disabled=True,
            # on_click=save_candidate,
        )

        pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(pick_files_dialog)
        self.upload_button = ft.TextButton(
            text="Upload Image",
            icon=ft.icons.FILE_UPLOAD_ROUNDED,
            on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True, file_type=ft.FilePickerFileType.IMAGE),
        )

        self.qualification_dropdown_values()

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

    def unsaved_dialogs(self):
        def on_close(e):
            alertdialog.open = False
            self.page.update()

        def discard(e):
            from .candidate_home import candidate_home_page
            alertdialog.open = False
            self.page.update()
            sleep(0.2)
            self.content_column.clean()
            self.content_column.update()
            candidate_home_page(self.page, self.content_column, self.title_text)
            self.change_values()

        alertdialog = ft.AlertDialog(
            modal=True,
            content=ft.Text(
                value="Your changes have not been saved",
            ),
            actions=[
                ft.TextButton(
                    text="Discard",
                    on_click=discard,
                ),
                ft.TextButton(
                    text="Save",
                    on_click=on_close,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = alertdialog
        alertdialog.open = True
        self.page.update()


def candidate_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    obj = CandidateHomePage(page, content_column, title_text)

    def back_candidate_add_page(e):
        obj.back_candidate_home()

    def can(e):
        from .category import category_home_page
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
    back_candidate_home_button = ft.IconButton(
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
                        back_candidate_home_button,
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
                obj.build(),
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
