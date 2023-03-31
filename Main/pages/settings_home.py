import flet as ft

election_expand = False


def settings_home_page(page: ft.Page, content_column: ft.Column, title_text: ft.Text):
    title_text.value = "Settings"

    # Text
    # Text & Buttons
    main_tittle_text = ft.Text(
        value="Settings",
        size=35,
        weight=ft.FontWeight.BOLD,
        italic=True,
    )

    icon_election_1 = ft.Icon(
        name=ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED,
        size=25,
    )

    def election_settings_option(e):
        global election_expand
        c3.disabled = True
        page.update()
        h1.height = 120 if h1.height == 45 else 45
        if election_expand is False:
            election_expand = True
            election_column_data2 = ft.Container(
                content=ft.Column([ft.Text("Clickable transparent with Ink"), ]),
                margin=2,
                padding=5,
                alignment=ft.alignment.center,
                height=50,
                border_radius=10,
                ink=True,
                on_click=lambda a: print("Clickable transparent with Ink clicked!"),
            )
            icon_election_1.name = ft.icons.KEYBOARD_ARROW_UP_ROUNDED
            c1.controls.append(election_column_data2)
            page.update()
        else:
            election_expand = False
            icon_election_1.name = ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED
            c1.controls = [c3]
            page.update()
        c3.disabled = False
        page.update()

    c3 = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Divider(),
                            ],
                            width=20
                        ),
                        ft.Text(
                            value="Election Settings",
                            size=20,
                        ),
                        ft.Column(
                            [
                                ft.Divider(),
                            ],
                            expand=True,
                        ),
                        icon_election_1,
                        ft.Column(
                            [
                                ft.Divider(),
                            ],
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
        on_click=election_settings_option,
    )

    c1 = ft.Column(
        [
            c3,
        ]
    )

    h1 = ft.Container(
        content=c1,
        border_radius=5,
        margin=3,
        border=ft.border.all(0.2, ft.colors.SECONDARY),
        alignment=ft.alignment.center,
        on_click=election_settings_option,
        height=45,
        animate=ft.animation.Animation(400, ft.AnimationCurve.DECELERATE)
    )

    settings_column_data = ft.Column(
        [
            h1
        ],
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
    )

    content_column.controls = [
        ft.Column(
            [
                ft.Row(
                    [
                        main_tittle_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(
                    height=5,
                    thickness=3,
                ),
                settings_column_data,
            ]
        )
    ]

    page.update()
