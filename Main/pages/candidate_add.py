import os
import glob
import shutil
import random
import string
from time import sleep
import flet as ft
import pandas as pd

from .category import category_add_page
from ..service.scr.loc_file_scr import file_data
import Main.service.scr.election_scr as ee
import Main.service.user.login_enc as cc

list_cand_data = ['', '', '', '']
save_button = ft.TextButton(
    text='Save',
    disabled=True,
)
alertdialog_candidate_add = None


def candidate_add_page(page: ft.Page):
    global alertdialog_candidate_add

    def add_cat(e):
        alertdialog_candidate_add.open = False
        page.update()
        sleep(0.2)
        category_add_page(page, 'candidate')

    def on_close(e):
        global list_cand_data
        alertdialog_candidate_add.open = False
        page.update()
        if list_cand_data[1] is not False:
            if len(list_cand_data[1]) != 0:
                try:
                    os.remove(fr'{ee.current_election_path}/images/{list_cand_data[1]}')
                except FileNotFoundError:
                    pass
        list_cand_data = ['', '', '', '', '']

    alertdialog_candidate_add = ft.AlertDialog(
        modal=True,
        title=None,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    value="Add Candidate",
                                    weight=ft.FontWeight.BOLD,
                                    size=25,
                                    font_family='Verdana',
                                ),
                            ],
                            expand=True,
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.CLOSE_ROUNDED,
                                    tooltip="Close",
                                    on_click=on_close,
                                )
                            ]
                        )
                    ]
                ),
                build(page)
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            height=360,
            width=650,
        ),
        actions=[
            ft.TextButton(
                text="Add new category",
                on_click=add_cat,
            ),
            save_button,
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    page.dialog = alertdialog_candidate_add
    alertdialog_candidate_add.open = True
    page.update()


def build(page: ft.Page):
    global list_cand_data

    def disable_button(e):
        global list_cand_data
        on_qualification_change()
        if len(name_entry.value) != 0:
            list_cand_data[0] = name_entry.value
            if qualification_dropdown.value is not None:
                if qualification_dropdown.value != "No Records":
                    list_cand_data[2] = qualification_dropdown.value
                    if category_dropdown.value is not None:
                        if category_dropdown.value != "Select Candidate Qualification":
                            list_cand_data[3] = category_dropdown.value
                            save_button.disabled = False
                        else:
                            save_button.disabled = True
                    else:
                        save_button.disabled = True
                else:
                    save_button.disabled = True
            else:
                save_button.disabled = True
        else:
            save_button.disabled = True
        try:
            save_button.update()
        except AssertionError:
            pass

    def save(e):
        global list_cand_data, alertdialog_candidate_add
        alertdialog_candidate_add.open = False
        page.splash = ft.ProgressBar()
        page.update()
        from ..service.files.write_files import add_candidate
        from ..functions.snack_bar import snack_bar1
        sleep(0.2)
        if list_cand_data[1] is not False:
            if len(list_cand_data[1]) == 0:
                image_data = False
            else:
                image_data = list_cand_data[1]
        else:
            image_data = False
        add_candidate([name_entry.value, category_dropdown.value, True, qualification_dropdown.value, image_data,
                       cc.teme_data[1]])
        page.splash = None
        page.update()
        from .candidate_home import display_candidate
        display_candidate(page)
        snack_bar1(page, "Successfully Added")
        list_cand_data = ['', '', '', '', '']

    save_button.on_click = save

    category_df = pd.read_csv(ee.current_election_path + rf'/{file_data["category_data"]}')
    candidate_image_destination = ee.current_election_path + r'/images'

    def on_qualification_change():
        temp_list3: list = []
        if qualification_dropdown.value is not None:
            if qualification_dropdown.value != "No Records":
                for j in list(category_df[category_df.qualification == qualification_dropdown.value].values):
                    temp_list3.append(ft.dropdown.Option(j[1]))
            else:
                temp_list3.append(ft.dropdown.Option("Select Candidate Qualification"))
        else:
            temp_list3.append(ft.dropdown.Option("Select Candidate Qualification"))

        category_dropdown.options = temp_list3
        page.update()

    # Input Field
    name_entry = ft.TextField(
        hint_text="Enter the Candidate name",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        error_style=ft.TextStyle(font_family='Verdana'),
        autofocus=True,
        capitalization=ft.TextCapitalization.WORDS,
        prefix_icon=ft.icons.PERSON_ROUNDED,
        on_change=disable_button,
    )

    qualification_dropdown = ft.Dropdown(
        hint_text="Choose Candidate Qualification",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        text_style=ft.TextStyle(font_family='Verdana'),
        color=ft.colors.BLACK,
        on_change=disable_button,
    )

    category_dropdown = ft.Dropdown(
        hint_text="Choose Candidate Category",
        width=350,
        border=ft.InputBorder.OUTLINE,
        border_radius=9,
        text_style=ft.TextStyle(font_family='Verdana'),
        color=ft.colors.BLACK,
        options=[
            ft.dropdown.Option("Select Candidate Qualification"),
        ],
        prefix_icon=ft.icons.CATEGORY_ROUNDED,
        on_change=disable_button,
    )

    container = ft.Container(
        content=ft.Text("Upload Image", font_family='Verdana'),
        width=200,
        height=250,
        alignment=ft.alignment.center,
        border=ft.border.all(1, ft.colors.BLACK),
        border_radius=10,
        image_fit=ft.ImageFit.COVER,
    )

    temp_list1: list = []
    if not category_df.empty:
        for i in list(category_df['qualification'].unique()):
            temp_list1.append(ft.dropdown.Option(i))
    else:
        temp_list1.append(ft.dropdown.Option("Select Candidate Qualification"))

    qualification_dropdown.options = temp_list1

    temp_list2: list = []
    if not category_df.empty:
        for i in list(category_df['category'].unique()):
            temp_list2.append(ft.dropdown.Option(i))
    else:
        temp_list2.append(ft.dropdown.Option("No Category Records"))

    category_dropdown.options = temp_list2

    if len(list_cand_data[0]) != 0:
        name_entry.value = list_cand_data[0]

    if len(list_cand_data[2]) != 0:
        qualification_dropdown.value = list_cand_data[2]

    if len(list_cand_data[3]) != 0:
        category_dropdown.value = list_cand_data[3]

    if len(list_cand_data[1]) != 0:
        container.image_src = candidate_image_destination + rf'/{list_cand_data[1]}'
        container.content = None

    def pick_files_result(e: ft.FilePickerResultEvent):
        global list_cand_data
        from ..functions.dialogs import error_dialogs
        candidate_image_destination1 = ee.current_election_path + r'/images'

        if list_cand_data[1] is not False:
            if len(list_cand_data[1]) != 0:
                candidate_image_destination1 += rf'/{list_cand_data[1]}'
                try:
                    os.remove(candidate_image_destination1)
                except FileNotFoundError:
                    pass

        source = string.ascii_letters + string.digits
        rand = ''.join((random.choice(source)) for _ in range(5))
        candidate_selected_image_name = f'{rand}' + "".join(map(lambda f: f.name, e.files)) if e.files else False
        candidate_selected_file_path = ", ".join(map(lambda f: f.path, e.files)) if e.files else False
        list_cand_data[1] = candidate_selected_image_name
        if candidate_selected_image_name is not False:
            candidate_image_destination1 = ee.current_election_path + r'/images' + rf'/{candidate_selected_image_name}'
            try:
                if not os.path.exists(candidate_image_destination1):
                    for jpgfile in glob.iglob(os.path.join(candidate_selected_file_path, candidate_selected_file_path)):
                        shutil.copy(candidate_selected_file_path, candidate_image_destination1)
                    container.content = ft.Text()
                    container.update()
                    container.image_src = candidate_image_destination1
                    container.update()
                else:
                    error_dialogs(page, "001")
            except OSError:
                container.content = ft.Text("Upload Image", font_family='Verdana', )
                container.update()
                list_cand_data[1] = ''
                error_dialogs(page, "002")
        else:
            container.image_src = None
            container.content = ft.Text("Upload canceled!", font_family='Verdana', )
            container.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    upload_button = ft.TextButton(
        text="Upload Image",
        icon=ft.icons.FILE_UPLOAD_ROUNDED,
        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True, file_type=ft.FilePickerFileType.IMAGE),
    )

    main_column = ft.Row(
        [
            ft.Column(
                [

                    ft.Row(
                        [
                            ft.Column(
                                [
                                    container,
                                    upload_button,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    name_entry,
                                    qualification_dropdown,
                                    category_dropdown,
                                ],
                                spacing=40,
                            )
                        ],
                        height=300,
                        spacing=50,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
    )

    return main_column
