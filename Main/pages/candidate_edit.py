import os
import random
from time import sleep
import string
import flet as ft
import pandas as pd

from Main.authentication.scr.loc_file_scr import file_data
import Main.authentication.scr.election_scr as ee


class CandidateEditPage:

    def __init__(self, page: ft.Page, content_column: ft.Column, title_text: ft.Text, index_val):
        super().__init__()
        self.content_column = content_column
        self.title_text = title_text
        self.page = page
        self.index_val = index_val
        self.candidate_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')
        self.candidate_data = self.candidate_df.loc[self.index_val].values
        self.candidate_selected_image_name = self.candidate_data[5]
        self.candidate_selected_file_path = None
        self.candidate_image_destination = ee.current_election_path + rf'\images\{self.candidate_data[5]}'

        # Input Fields
        self.name_entry = ft.TextField(
            hint_text="Enter the Candidate name",
            width=450,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            border_color=ft.colors.SECONDARY,
            autofocus=True,
            capitalization=ft.TextCapitalization.WORDS,
            prefix_icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
            on_change=self.disable_save_button,
            value=self.candidate_data[1]
        )

        self.qualification_dropdown = ft.Dropdown(
            hint_text="Choose Candidate Qualification",
            width=450,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            on_change=self.on_change_qualification,
            prefix_icon=ft.icons.CATEGORY_ROUNDED,
            border_color=ft.colors.SECONDARY,
        )

        self.category_dropdown = ft.Dropdown(
            hint_text="Choose Candidate Category",
            width=450,
            on_change=self.disable_save_button,
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

        if self.candidate_data[5] != False:
            self.container.content = ft.Text()
            self.container.image_src = self.candidate_image_destination
            self.container.image_fit = ft.ImageFit.COVER

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
            option_list1.append(ft.dropdown.Option(self.candidate_data[4]))

        self.qualification_dropdown.options = option_list1
        self.qualification_dropdown.value = self.candidate_data[4]
        self.on_change_qualification('e')

    def on_change_qualification(self, e):
        option_list2: list = []
        temp_list1: list = []

        if self.qualification_dropdown.value is not None:
            if self.qualification_dropdown.value != "No Category Records":
                cur_val = self.category_df[self.category_df.qualification == self.qualification_dropdown.value].values
                for j in range(len(cur_val)):
                    if cur_val[j][1] not in temp_list1:
                        option_list2.append(ft.dropdown.Option(cur_val[j][1]))
                        temp_list1.append(cur_val[j][1])
            else:
                from ..functions.dialogs import message_dialogs
                message_dialogs(self.page, "No Category Recodes")
        else:
            option_list2.append(ft.dropdown.Option("Select Candidate Qualification"))
            option_list2.append(ft.dropdown.Option(self.candidate_data[2]))

        self.category_dropdown.options = option_list2
        if self.qualification_dropdown.value == self.candidate_data[4]:
            self.category_dropdown.value = self.candidate_data[2]
        else:
            self.category_dropdown.value = None
        try:
            self.category_dropdown.update()
        except AssertionError:
            pass
        self.disable_save_button(e)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        from ..functions.dialogs import error_dialogs
        if self.candidate_selected_image_name is not False or self.candidate_selected_image_name != self.candidate_data[
            5]:
            try:
                os.replace(self.candidate_image_destination, self.candidate_selected_file_path)
            except FileNotFoundError:
                pass
            except TypeError:
                pass

        source = string.ascii_letters + string.digits
        rand = ''.join((random.choice(source)) for i in range(5))
        self.candidate_selected_image_name = f'{rand}' + "".join(map(lambda f: f.name, e.files)) if e.files else False
        self.candidate_selected_file_path = ", ".join(map(lambda f: f.path, e.files)) if e.files else False

        if self.candidate_selected_image_name is not False:
            self.candidate_image_destination = ee.current_election_path + rf'\images\{self.candidate_selected_image_name}'
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
            if self.candidate_data[5] != False:
                self.container.content = ft.Text()
                self.container.image_src = self.candidate_image_destination
                self.container.image_fit = ft.ImageFit.COVER
                self.candidate_selected_image_name = self.candidate_data[5]
            else:
                self.container.image_src = None
                self.container.content = ft.Text("Upload canceled!")
                self.container.update()
        self.disable_save_button(e)

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
        if self.name_entry.value != self.candidate_data[1]:
            self.unsaved_edit_dialogs()
        elif self.candidate_selected_image_name != self.candidate_data[5]:
            self.unsaved_edit_dialogs()
        elif self.qualification_dropdown.value != self.candidate_data[4]:
            self.unsaved_edit_dialogs()
        elif self.category_dropdown.value != self.candidate_data[2]:
            self.unsaved_edit_dialogs()
        else:
            self.content_column.clean()
            self.content_column.update()
            candidate_home_page(self.page, self.content_column, self.title_text)

    def disable_save_button(self, e):
        list_value: list = [False, False, False, False]
        if self.name_entry.value != self.candidate_data[1]:
            if len(self.name_entry.value) != 0:
                self.name_entry.error_text = None
                self.name_entry.update()
                list_value[0] = True
            else:
                self.name_entry.error_text = "Enter the Name"
                self.name_entry.update()
        else:
            list_value[0] = False
        if self.candidate_selected_image_name != self.candidate_data[5]:
            list_value[1] = True
        else:
            list_value[1] = False
        if self.qualification_dropdown.value != self.candidate_data[4]:
            list_value[2] = True
        else:
            list_value[2] = False
        if self.category_dropdown.value != self.candidate_data[2]:
            if len(self.category_dropdown.value) != 0:
                self.category_dropdown.error_text = None
                self.category_dropdown.update()
                list_value[3] = True
            else:
                self.category_dropdown.error_text = "Select a Category"
                self.category_dropdown.update()
                list_value[3] = False
        else:
            list_value[3] = False
        if True in list_value:
            self.save_button.disabled = False
        else:
            self.save_button.disabled = True
        try:
            self.save_button.update()
        except AssertionError:
            pass

    def save_data(self, e):
        if len(self.name_entry.value) != 0:
            if len(self.category_dropdown.value) != 0:
                self.edit_save_dialogs()
            else:
                self.category_dropdown.error_text = "Select a Category"
                self.category_dropdown.update()
        else:
            self.name_entry.error_text = "Enter the Name"
            self.name_entry.focus()
            self.name_entry.update()

    def build(self):
        self.save_button = ft.ElevatedButton(
            text="Save Changes",
            height=50,
            width=150,
            disabled=True,
            on_click=self.save_data,
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

    def unsaved_edit_dialogs(self):
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
            if self.candidate_selected_image_name != self.candidate_data[5]:
                self.change_values()

        alertdialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value="Discard changes?",
            ),
            content=ft.Text(
                value="Your changes not been saved",
            ),
            actions=[
                ft.TextButton(
                    text="Keep editing",
                    on_click=on_close,
                ),
                ft.TextButton(
                    text="Discard",
                    on_click=discard,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = alertdialog
        alertdialog.open = True
        self.page.update()

    def edit_save_dialogs(self):
        def on_close(e):
            alertdialog.open = False
            self.page.update()

        def save_changes(e):
            alertdialog.open = False
            self.page.update()
            self.save_button.disabled = True
            self.page.splash = ft.ProgressBar()
            self.page.update()
            from ..authentication.files.write_files import candidate_edit
            from ..functions.snack_bar import snack_bar1
            from ..functions.dialogs import loading_dialogs
            from .candidate_home import candidate_home_page
            sleep(0.1)
            loading_dialogs(self.page, "Saving Changes...", 1)
            candidate_edit([self.name_entry.value, self.category_dropdown.value, self.qualification_dropdown.value,
                            self.candidate_selected_image_name], self.index_val)
            self.page.splash = None
            self.page.update()
            self.content_column.clean()
            self.content_column.update()
            candidate_home_page(self.page, self.content_column, self.title_text)
            snack_bar1(self.page, "Successfully Updated")

        alertdialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value="Save your changes?",
            ),
            content=ft.Text(
                value="This record will be updated.",
            ),
            actions=[
                ft.TextButton(
                    text="Ok",
                    on_click=save_changes,
                ),
                ft.TextButton(
                    text="Cancel",
                    on_click=on_close,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = alertdialog
        alertdialog.open = True
        self.page.update()


def candidate_edit_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text, index_val):
    obj = CandidateEditPage(page, content_column, title_text, index_val)

    def back_candidate_add_page(e):
        obj.back_candidate_home()

    def can(e):
        from .category import category_home_page
        content_column.clean()
        content_column.update()
        category_home_page(page, content_column, title_text)

    title_text.value = "Candidate > Edit Candidate"

    # Main Text
    main_candidate_edit_text = ft.Text(
        value="Edit Candidate",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    # Button
    back_candidate_home_button = ft.IconButton(
        tooltip="Back",
        icon=ft.icons.ARROW_BACK_ROUNDED,
        on_click=back_candidate_add_page,
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
                        main_candidate_edit_text,
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
