import flet as ft

from .category import category_dialogs

ele_option_data_update = None


class ElectionSettingsMenu:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page


def election_settings_page(page: ft.Page, main_column: ft.Column):
    global ele_option_data_update
    option_menu = ElectionSettingsMenu(page)
    ele_option_data_update = option_menu

    category_option = ft.Card(
        ft.Container(
            ft.ListTile(
                title=ft.Text(
                    value=f"Category",
                    font_family='Verdana',
                ),
                trailing=ft.Icon(
                    name=ft.icons.NAVIGATE_NEXT_ROUNDED,
                    size=25,
                ),
                on_click=lambda _: category_dialogs(page),
            ),
            blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
            padding=ft.padding.symmetric(vertical=3.5),
            border_radius=10,
        ),
        elevation=0,
        color=ft.colors.with_opacity(0.4, '#44CCCCCC'),
    )

    main_column.controls = [
        ft.Column(
            [
                ft.Row(height=3),
                category_option,
            ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE
        )
    ]

    page.splash = None
    page.update()

# def update_settings_data():
#     ele_option_data_update.change_in_data()
