import flet as ft

from Main.functions.animations import settings_admin_options_animation


class SettingsAdminOptions(ft.UserControl):
    def __init__(self, page: ft.Page, content_column: ft.Column):
        super().__init__()
        self.button_container = None
        self.admin_expand = False
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
        settings_admin_options_animation(self.main_container)
        if not self.admin_expand:
            self.admin_expand = True
            self.icon_election.name = ft.icons.KEYBOARD_ARROW_UP_ROUNDED
            self.main_container.update()
        else:
            self.icon_election.name = ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED
            self.main_column.controls = [self.button_container]
            self.admin_expand = False
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
                                value="Admin Settings",
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

        self.main_column.controls = [
            self.button_container
        ]

        return ft.Column(
            [
                self.main_container
            ]
        )
