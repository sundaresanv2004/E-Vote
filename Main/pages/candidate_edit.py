import os
import glob
import shutil
import random
import string
from time import sleep
import flet as ft
import pandas as pd

from .candidate_profile import candidate_profile_page
from ..service.scr.loc_file_scr import file_data
import Main.service.scr.election_scr as ee

list_cand_data_edit = ['', '', '', '']
save_button = ft.TextButton(
    text='Save Changes',
    disabled=True,
)
alertdialog_candidate_edit = None


def candidate_edit_page(page: ft.Page, index_val, page_view):
    global alertdialog_candidate_edit
    candidate_df = pd.read_json(ee.current_election_path + rf'/{file_data["candidate_data"]}', orient='table')
    candidate_data = candidate_df.loc[index_val].values

    def on_close_edit(e):
        global list_cand_data_edit
        alertdialog_candidate_edit.open = False
        page.update()
        if list_cand_data_edit[1] is not False:
            if len(list_cand_data_edit[1]) != 0:
                if list_cand_data_edit[1] != candidate_data[5]:
                    try:
                        os.remove(fr'{ee.current_election_path}/images/{list_cand_data_edit[1]}')
                    except FileNotFoundError:
                        pass
        list_cand_data_edit = ['', '', '', '', '']
        sleep(0.2)
        if page_view:
            candidate_profile_page(page, index_val)

    alertdialog_candidate_edit = ft.AlertDialog(
        modal=True,
        title=None,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    value="Edit Candidate",
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
                                    on_click=on_close_edit,
                                )
                            ]
                        )
                    ]
                ),
                build(page, index_val, page_view)
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            height=360,
            width=650,
        ),
        actions=[
            save_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    page.dialog = alertdialog_candidate_edit
    alertdialog_candidate_edit.open = True
    page.update()


def build(page: ft.Page, index_val, page_view):
    global list_cand_data_edit
    candidate_df = pd.read_json(ee.current_election_path + rf'/{file_data["candidate_data"]}', orient='table')
    candidate_data = candidate_df.loc[index_val].values
    list_cand_data_edit[0] = candidate_data[1]
    list_cand_data_edit[1] = candidate_data[5]
    list_cand_data_edit[2] = candidate_data[4]
    list_cand_data_edit[3] = candidate_data[2]

    def disable_button(e):
        global list_cand_data_edit
        on_qualification_change()
        list_value: list = [False, False, False, False]
        if name_entry.value != candidate_data[1]:
            if len(name_entry.value) != 0:
                name_entry.error_text = None
                name_entry.update()
                list_value[0] = True
            else:
                name_entry.error_text = "Enter the Name"
                name_entry.update()
        else:
            list_value[0] = False
        if list_cand_data_edit[1] != candidate_data[5]:
            list_value[1] = True
        else:
            list_value[1] = False
        if qualification_dropdown.value != candidate_data[4]:
            list_value[2] = True
        else:
            list_value[2] = False

        if category_dropdown.value != candidate_data[2]:
            if len(category_dropdown.value) != 0:
                category_dropdown.error_text = None
                category_dropdown.update()
                list_value[3] = True
            else:
                category_dropdown.error_text = "Select a Category"
                category_dropdown.update()
                list_value[3] = False
        else:
            list_value[3] = False
        if True in list_value:
            save_button.disabled = False
        else:
            save_button.disabled = True
        save_button.update()

    def save(e):
        global list_cand_data_edit, alertdialog_candidate_edit
        alertdialog_candidate_edit.open = False
        page.splash = ft.ProgressBar()
        page.update()
        from ..service.files.write_files import candidate_edit
        from ..functions.snack_bar import snack_bar1
        sleep(0.2)
        if candidate_data[5] is not False:
            if list_cand_data_edit[1] != candidate_data[5]:
                try:
                    os.remove(fr'{ee.current_election_path}/images/{candidate_data[5]}')
                except FileNotFoundError:
                    pass
        if list_cand_data_edit[1] is not False:
            if len(list_cand_data_edit[1]) == 0:
                image_data1 = False
            else:
                image_data1 = list_cand_data_edit[1]
        else:
            image_data1 = False
        candidate_edit([name_entry.value, category_dropdown.value, qualification_dropdown.value,
                        image_data1], index_val)
        page.splash = None
        page.update()
        from .candidate_home import display_candidate
        display_candidate(page)
        if page_view:
            candidate_profile_page(page, index_val)
        snack_bar1(page, "Successfully Updated")
        list_cand_data_edit = ['', '', '', '', '']

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

    if len(list_cand_data_edit[0]) != 0:
        name_entry.value = list_cand_data_edit[0]

    if len(list_cand_data_edit[2]) != 0:
        qualification_dropdown.value = list_cand_data_edit[2]

    if len(list_cand_data_edit[3]) != 0:
        category_dropdown.value = list_cand_data_edit[3]

    if list_cand_data_edit[1] != False:
        if len(list_cand_data_edit[1]) != 0:
            container.image_src = candidate_image_destination + rf'/{list_cand_data_edit[1]}'
            container.content = None

    def pick_files_result(e: ft.FilePickerResultEvent):
        global list_cand_data_edit
        from ..functions.dialogs import error_dialogs

        source = string.ascii_letters + string.digits
        rand = ''.join((random.choice(source)) for _ in range(5))
        candidate_selected_image_name = f'{rand}' + "".join(map(lambda f: f.name, e.files)) if e.files else False
        candidate_selected_file_path = ", ".join(map(lambda f: f.path, e.files)) if e.files else False
        list_cand_data_edit[1] = candidate_selected_image_name
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
                list_cand_data_edit[1] = ''
                error_dialogs(page, "002")
        else:
            container.image_src = None
            container.content = ft.Text("Upload canceled!", font_family='Verdana', )
            container.update()
        disable_button(e)

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
