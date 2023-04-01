from time import sleep
import flet as ft

from Main.functions.animations import settings_election_options_animation


class SettingsElectionOptions(ft.UserControl):
    def __init__(self, page: ft.Page, content_column: ft.Column):
        super().__init__()
        self.create_new_election = None
        self.add_category_option = None
        self.button_container = None
        self.election_expand = False
        self.main_column = ft.Column()
        self.main_container = ft.Container(
            border_radius=5,
            content=self.main_column,
            margin=3,
            border=ft.border.all(0.5, ft.colors.SECONDARY),
            height=45,
            animate=ft.animation.Animation(400, ft.AnimationCurve.DECELERATE)
        )
        self.icon_election = ft.Icon(
            name=ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            size=25,
        )

    # Functions
    def election_settings_option(self, e):
        settings_election_options_animation(self.main_container)
        sleep(0.1)
        if not self.election_expand:
            self.election_expand = True

            self.icon_election.name = ft.icons.KEYBOARD_ARROW_UP_ROUNDED
            temp_list: list = [self.add_category_option, self.create_new_election]
            for i in temp_list:
                self.main_column.controls.append(i)
            self.main_container.update()
        else:
            self.icon_election.name = ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED
            self.main_column.controls = [self.button_container]
            self.election_expand = False
            self.main_container.update()

    def build(self):
        # Main Button
        self.button_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                width=20
                            ),
                            ft.Text(
                                value="Election Settings",
                                size=20,
                            ),
                            ft.Column(
                                expand=True,
                            ),
                            self.icon_election,
                            ft.Column(
                                width=30
                            ),
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                height=35,
            ),
            border_radius=3,
            padding=5,
            ink=True,
            alignment=ft.alignment.center,
            on_click=self.election_settings_option,
        )

        self.add_category_option = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Manage Category Details",
                                size=20,
                            )
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                text="Manage",
                                icon=ft.icons.SETTINGS_SUGGEST_ROUNDED,
                            )
                        ]
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            border=ft.border.all(0.1, ft.colors.SECONDARY)
        )

        self.create_new_election = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Create an Election",
                                size=20,
                            )
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                text="Create",
                                icon=ft.icons.ADD_ROUNDED,
                            )
                        ]
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            alignment=ft.alignment.center,
            height=70,
            border=ft.border.all(0.1, ft.colors.SECONDARY)
        )

        self.main_column.controls = [
            self.button_container
        ]

        return ft.Column(
            [
                self.main_container
            ]
        )
