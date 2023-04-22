import os
import random
import string
from time import sleep
import pandas as pd
import flet as ft
from datetime import date

import Main.functions.theme as tt
from ..authentication.scr.loc_file_scr import registration_text_data
from ..functions.animations import register_container_animation
from ..functions.date_time import months_
from Main.authentication.scr.loc_file_scr import file_data
import Main.authentication.scr.election_scr as ee


def register_home_page(page: ft.Page, menu_container: ft.Container):
    import Main.authentication.scr.election_scr as ee
    from Main.authentication.scr.loc_file_scr import file_data

    def on_change_button(e):
        if checkbox_terms1.value is True and checkbox_terms2.value is True:
            submit_button.disabled = False
        else:
            submit_button.disabled = True
        submit_button.update()

    def back(e):
        back_button.disabled = True
        menu_container.clean()
        page.update()
        from Main.pages.menu import menu_page
        register_container_animation(menu_container)
        sleep(0.1)
        menu_page(page, menu_container)

    def submit_on_clicked(e):
        page.clean()
        register_page(page)

    # Buttons
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip='Back',
        on_click=back,
    )

    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')

    submit_button = ft.ElevatedButton(
        text="Next",
        height=50,
        width=120,
        disabled=True,
        on_click=submit_on_clicked,
    )

    # Input Filed
    checkbox_terms1 = ft.Checkbox(
        label="I have carefully reviewed and understood the information provided above.",
        value=False,
        on_change=on_change_button,
    )

    checkbox_terms2 = ft.Checkbox(
        label="I assure you that I will answer all details truthfully and to the best of my knowledge.",
        value=False,
        on_change=on_change_button,
    )

    container_data = ft.Container(
        margin=20,
        padding=10,
        alignment=ft.alignment.center
    )

    column_data1 = ft.Column()

    temp_a = ele_ser.loc['registration_from'].values[0]
    day1, month1, year1 = [x for x in temp_a.split('/')]
    d1 = date(int(year1), months_.index(month1) + 1, int(day1))

    temp_a = ele_ser.loc['registration_to'].values[0]
    day2, month2, year2 = [x for x in temp_a.split('/')]
    d2 = date(int(year2), months_.index(month2) + 1, int(day2))

    td = date.today()

    if d1 <= td <= d2:
        container_data.content = ft.Column(
            [
                ft.Markdown(
                    registration_text_data,
                )
            ],
            width=700,
        )
        column_data1.controls = [
            ft.Column(
                [
                    checkbox_terms1,
                    checkbox_terms2,
                ],
            ),
            ft.Row(
                [
                    submit_button,
                ],
                alignment=ft.MainAxisAlignment.END,
                width=790,
            )
        ]
    elif td < d1:
        container_data.content = ft.Column(
            [
                ft.Text(
                    value=f"Please note that the registration for the election has not started yet. You will be able "
                          f"to register for the election from {ele_ser.loc['registration_from'].values[0]} onwards.",
                    size=20,
                )
            ],
            width=700,
        )
    elif td > d2:
        container_data.content = ft.Column(
            [
                ft.Text(
                    value="The registration for the election has ended, and we are no longer accepting any new "
                          "registrations. Please get in touch with the election department if you require any more "
                          "information.",
                    size=20,
                )
            ],
            width=700,
        )

    # alignment and data
    all_done_data_column = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            back_button,
                        ],
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                value="Make a Difference",
                                size=30,
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
                height=5,
            ),
            ft.Column(
                [
                    container_data,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Column(
                height=10,
            ),
            column_data1,
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


class CandidateAddPage:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
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
            capitalization=ft.TextCapitalization.WORDS,
            prefix_icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
            on_change=self.disable_save_button,
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

    def qualification_dropdown_values(self):
        option_list1: list = []
        temp_list: list = []

        if self.category_df.empty is not True:
            for i in range(len(self.category_df)):
                if self.category_df.loc[i].values[2] not in temp_list:
                    option_list1.append(ft.dropdown.Option(self.category_df.loc[i].values[2]))
                    temp_list.append(self.category_df.loc[i].values[2])
        else:
            option_list1.append(ft.dropdown.Option("No Qualification Records"))

        self.qualification_dropdown.options = option_list1

    def on_change_qualification(self, e):
        option_list2: list = []
        temp_list1: list = []

        if self.qualification_dropdown.value is not None:
            if self.qualification_dropdown.value != "No Qualification Records":
                cur_val = self.category_df[self.category_df.qualification == self.qualification_dropdown.value].values
                for j in range(len(cur_val)):
                    if cur_val[j][1] not in temp_list1:
                        option_list2.append(ft.dropdown.Option(cur_val[j][1]))
                        temp_list1.append(cur_val[j][1])
            else:
                self.went_wrong()
        else:
            option_list2.append(ft.dropdown.Option("Select Candidate Qualification"))

        self.category_dropdown.options = option_list2
        self.category_dropdown.update()
        self.disable_save_button(e)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        from ..functions.dialogs import error_dialogs
        if self.candidate_selected_image_name is not False:
            try:
                os.replace(self.candidate_image_destination, self.candidate_selected_file_path)
            except FileNotFoundError:
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
        from main import main
        if len(self.name_entry.value) != 0:
            self.unsaved_dialogs()
        elif self.candidate_selected_image_name is not False:
            self.unsaved_dialogs()
        else:
            self.page.clean()
            self.page.update()
            main(self.page)

    def disable_save_button(self, e):
        if len(self.name_entry.value) != 0:
            if self.qualification_dropdown.value is not None:
                if self.qualification_dropdown.value != "No Category Records":
                    if self.category_dropdown.value is not None:
                        if self.category_dropdown.value != "Select Candidate Qualification":
                            self.save_button.disabled = False
                        else:
                            self.save_button.disabled = True
                    else:
                        self.save_button.disabled = True
                else:
                    self.save_button.disabled = True
            else:
                self.save_button.disabled = True
        else:
            self.save_button.disabled = True
        self.save_button.update()

    def save_data(self):
        self.save_button.disabled = True
        self.page.splash = ft.ProgressBar()
        self.page.update()
        from ..authentication.files.write_files import add_candidate
        from ..functions.dialogs import loading_dialogs
        from main import main
        sleep(0.1)
        loading_dialogs(self.page, "Saving...", 2)
        add_candidate([self.name_entry.value, self.category_dropdown.value, False, self.qualification_dropdown.value,
                       self.candidate_selected_image_name, "Registered"])
        self.page.splash = None
        self.page.update()
        self.page.clean()
        self.page.update()
        main(self.page)
        sleep(0.5)
        self.success()

    def build(self):
        self.save_button = ft.ElevatedButton(
            text="Save",
            height=50,
            width=150,
            disabled=True,
            on_click=self.make_sure,
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
            from main import main
            alertdialog.open = False
            self.page.update()
            sleep(0.2)
            self.page.clean()
            self.page.update()
            main(self.page)
            self.change_values()

        alertdialog = ft.AlertDialog(
            content=ft.Text(
                value="Your changes have not been saved",
            ),
            modal=True,
            actions=[
                ft.TextButton(
                    text="Save",
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

    def went_wrong(self):
        def on_close(e):
            from main import main
            alertdialog.open = False
            self.page.update()
            self.page.clean()
            self.page.update()
            main(self.page)

        alertdialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Something went wrong"),
            content=ft.Text(
                value="Oops! Something went wrong. Please try again later or \n"
                      "please reach out to the election department.",
            ),
            actions=[
                ft.TextButton(
                    text="Ok",
                    on_click=on_close,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = alertdialog
        alertdialog.open = True
        self.page.update()

    def make_sure(self, e):
        def on_close(e):
            alertdialog.open = False
            self.page.update()

        def on_save(e):
            alertdialog.open = False
            self.page.update()
            sleep(0.1)
            self.save_data()

        alertdialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Make Sure"),
            content=ft.Text(
                value="Please ensure that all inputs are correct before submitting your form,\n "
                      "as changes cannot be made once it has been submitted.",
            ),
            actions=[
                ft.TextButton(
                    text="Save",
                    on_click=on_save,
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

    def success(self):
        def on_close(e):
            alertdialog.open = False
            self.page.update()

        alertdialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Successfully Registered"),
            content=ft.Text("Thank you for registering for the election.\n"
                            "Your submission has been successfully processed."),
            actions=[
                ft.TextButton(
                    text="Ok",
                    on_click=on_close,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = alertdialog
        alertdialog.open = True
        self.page.update()


def register_page(page: ft.Page):
    obj = CandidateAddPage(page)

    def back_candidate_page(e):
        obj.back_candidate_home()

    # Button
    back_candidate_home_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK_ROUNDED,
        tooltip="Back",
        on_click=back_candidate_page,
    )

    appbar = ft.AppBar(
        center_title=False,
        leading=back_candidate_home_button,
        title=ft.Text(value="Candidate Registration", size=20, weight=ft.FontWeight.BOLD),
        leading_width=50,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            tt.ThemeIcon(page)
        ],
    )

    content_column = ft.Column(
        [
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
    )

    page.add(
        appbar,
        content_column,
    )
