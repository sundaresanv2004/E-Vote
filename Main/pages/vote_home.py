import flet as ft


def vote_home_page(page: ft.Page):
    main_column = ft.Column(expand=True)

    container = ft.Container(
        image_fit=ft.ImageFit.COVER,
        image_src="Main/assets/images/background-3.png",
        margin=-10,
        expand=True,
        content=ft.Column(
            [
                ft.Row(),
                main_column
            ],
        )
    )

    page.add(container)
    page.update()
