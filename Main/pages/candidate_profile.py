from time import sleep
import flet as ft
import pandas as pd

from ..service.scr.loc_file_scr import file_data
import Main.service.scr.election_scr as ee

index_val, ver_val = None, None


def candidate_profile_page(page: ft.Page, id_val):
    global index_val

    candidate_data_df = pd.read_json(ee.current_election_path + rf'\{file_data["candidate_data"]}', orient='table')
    candidate_image_destination = ee.current_election_path + r'\images'

    def on_close(e):
        alertdialog.open = False
        page.update()

    index_val = id_val

    def next_fun(e):
        global index_val
        index_val += 1
        content_change()
        page.update()

    def back_fun(e):
        global index_val
        index_val -= 1
        content_change()
        page.update()

    next_button = ft.IconButton(
        icon=ft.icons.NAVIGATE_NEXT_ROUNDED,
        icon_size=30,
        tooltip='Next',
        on_click=next_fun,
    )

    back_button = ft.IconButton(
        icon=ft.icons.KEYBOARD_ARROW_LEFT_ROUNDED,
        icon_size=30,
        tooltip="Previous",
        on_click=back_fun,
    )

    container = ft.Container(
        width=200,
        height=250,
        alignment=ft.alignment.center,
        border=ft.border.all(0.5, ft.colors.SECONDARY),
        border_radius=ft.border_radius.all(5),
    )

    def button_check():
        if index_val == 0:
            back_button.disabled = True
        else:
            back_button.disabled = False

        if index_val == candidate_data_df.index.max():
            next_button.disabled = True
        else:
            next_button.disabled = False

    def delete_on_click(e):
        alertdialog.open = False
        page.update()
        sleep(0.1)
        from .candidate_delete import delete_candidate_dialogs
        delete_candidate_dialogs(page, index_val, True)

    def edit_on_click(e):
        alertdialog.open = False
        page.update()
        sleep(0.2)
        from .candidate_edit import candidate_edit_page
        candidate_edit_page(page, index_val, True)

    title1 = ft.Text(
        weight=ft.FontWeight.BOLD,
        size=25,
        font_family='Verdana',
    )

    name_text = ft.Text(
        size=25,
        font_family='Verdana',
    )

    category_text = ft.Text(
        size=25,
        font_family='Verdana',
    )

    qualification_text = ft.Text(
        size=25,
        font_family='Verdana',
    )
    # verification_icon = ft.Icon(size=30)

    added_on_text = ft.Text(
        size=25,
        font_family='Verdana',
    )

    added_by_text = ft.Text(
        size=25,
        font_family='Verdana',
    )

    # def on_click_ver(e):
    #    pass

    # verify_text = ft.TextButton(on_click=on_click_ver)

    def content_change():
        global ver_val
        user_data = candidate_data_df.loc[index_val].values
        button_check()
        title1.value = f"Candidate ID: {user_data[0]}"
        name_text.value = f"Name: {user_data[1]}"
        category_text.value = f"Category: {user_data[2]}"
        qualification_text.value = f"Qualification: {user_data[4]}"
        added_by_text.value = f"Created by: {user_data[7]}"
        add_val = ''
        for i in range(10):
            add_val += user_data[6][i]
        added_on_text.value = f"Created on: {add_val}"
        ver_val = user_data[3]
        # if user_data[3] == True:
        #     verification_icon.color = ft.colors.GREEN_700
        #     verification_icon.name = ft.icons.DONE_ALL_ROUNDED
        #     verify_text.text = "Invalidate"
        #     verify_text.icon_color = ft.colors.RED_700
        #     verify_text.icon = ft.icons.NOT_INTERESTED_ROUNDED
        #     verify_text.tooltip = 'Invalidate'
        # else:
        #     verification_icon.name = ft.icons.CLOSE_ROUNDED
        #     verification_icon.color = ft.colors.RED_700
        #     verify_text.text = "Validate"
        #     verify_text.icon_color = ft.colors.GREEN_700
        #     verify_text.icon = ft.icons.DONE_ALL_ROUNDED
        #     verify_text.tooltip = 'Validate'

        if user_data[5] != False:
            container.content = ft.Text()
            container.image_src = candidate_image_destination + f'/{user_data[5]}'
            container.image_fit = ft.ImageFit.COVER
        else:
            container.image_src = None
            container.content = ft.Column(
                [
                    ft.Icon(
                        name=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                        size=40,
                    ),
                    ft.Text(
                        value="Image not found",
                        font_family='Verdana',
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                height=250,
                width=200,
            )

    content_change()

    edit_button = ft.TextButton(
        text="Edit",
        icon=ft.icons.EDIT_ROUNDED,
        tooltip="Edit",
        on_click=edit_on_click,
    )

    delete_button = ft.TextButton(
        text="Delete",
        icon=ft.icons.DELETE_ROUNDED,
        tooltip='Delete',
        on_click=delete_on_click,
    )
    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')
    if ele_ser.loc['lock_data'].values[0]:
        edit_button.disabled = True
        delete_button.disabled = True
        # verify_text.disabled = True

    alertdialog = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                title1,
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
                ft.Row(
                    [
                        back_button,
                        ft.Row(
                            [
                                container,
                                ft.Column(
                                    [
                                        name_text,
                                        category_text,
                                        qualification_text,
                                        # ft.Row([ft.Text(value="Verification: ", size=25,), verification_icon]),
                                        added_on_text,
                                        added_by_text,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=20,
                            width=560,
                            scroll=ft.ScrollMode.ADAPTIVE,
                        ),
                        next_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    width=670,
                    height=300,
                ),

            ],
            height=350,
            width=670,
        ),
        actions=[
            edit_button,
            delete_button,
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()
