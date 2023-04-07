from datetime import datetime, date
import flet as ft
import calendar
import pandas as pd

now = datetime.now()
hour = now.hour

if hour < 12:
    current_time = "Good Morning"
elif hour < 16:
    current_time = "Good Afternoon"
else:
    current_time = "Good Evening"

present_date = date.today()
present_year = present_date.year
present_month = present_date.month
present_day = present_date.day
months_ = list(calendar.month_name)[1:]

if present_month >= 6:
    current_academic_year = f'{present_year}-{present_year + 1}'
else:
    current_academic_year = f'{present_year - 1}-{present_year}'


class DateTimeField:

    def __init__(self):
        super().__init__()

        self.year_drop_down = ft.Dropdown(
            hint_text="Year",
            width=100,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            # on_change=self.on_change_qualification,
            border_color=ft.colors.SECONDARY,
            options=[
                ft.dropdown.Option(present_year - 1),
                ft.dropdown.Option(present_year),
                ft.dropdown.Option(present_year + 1),
                ft.dropdown.Option(present_year + 2),
                ft.dropdown.Option(present_year + 3),
            ],
        )

        self.months_drop_down = ft.Dropdown(
            hint_text="Month",
            width=150,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            border_color=ft.colors.SECONDARY,
        )

        month_list: list = []
        for i in months_:
            month_list.append(ft.dropdown.Option(i))
        self.months_drop_down.options = month_list

        self.days_drop_down = ft.Dropdown(
            hint_text="Day",
            width=100,
            border=ft.InputBorder.OUTLINE,
            border_radius=9,
            border_color=ft.colors.SECONDARY,
        )

        day_list: list = []
        for i in range(1, 32):
            day_list.append(ft.dropdown.Option(i))
        self.days_drop_down.options = day_list

    def save(self, from_val, to_val):
        pass


def datetime_field(page: ft.Page):
    import Main.authentication.scr.election_scr as ee
    from Main.authentication.scr.loc_file_scr import file_data

    from_obj = DateTimeField()
    to_obj = DateTimeField()

    ele_ser = pd.read_json(ee.current_election_path + fr"\{file_data['election_settings']}", orient='table')

    def save_on_click(e):
        if to_obj.year_drop_down.value is not None:
            to_obj.year_drop_down.error_text = None
            if to_obj.months_drop_down.value is not None:
                to_obj.months_drop_down.error_text = None
                if to_obj.days_drop_down.value is not None:
                    to_obj.days_drop_down.error_text = None
                    page.update()
                    # from
                    from_year = from_obj.year_drop_down.value
                    from_month = from_obj.months_drop_down.value
                    from_day = from_obj.days_drop_down.value
                    # to
                    to_year = to_obj.year_drop_down.value
                    to_month = to_obj.months_drop_down.value
                    to_day = to_obj.days_drop_down.value
                    from_date = f"{from_year}/{from_month}/{from_day}"
                    to_date = f"{to_year}/{to_month}/{to_day}"
                    if from_date <= to_date:
                        from ..authentication.files.settings_write import registration_date
                        registration_date(from_date, to_date)
                        alertdialog.open = False
                        page.update()
                    else:
                        to_obj.days_drop_down.error_text = "Invalid Date"
                        to_obj.months_drop_down.error_text = "Invalid Date"
                        to_obj.year_drop_down.error_text = "Invalid Date"
                        page.update()
                else:

                    to_obj.days_drop_down.error_text = "Day"
            else:
                to_obj.months_drop_down.error_text = "Month"
        else:
            to_obj.year_drop_down.error_text = "Year"
        page.update()

    if pd.isna(ele_ser.loc['registration_from'].values[0]) is True:
        from_obj.year_drop_down.value = present_year
        from_obj.months_drop_down.value = months_[present_month - 1]
        from_obj.days_drop_down.value = present_day
    else:
        temp_b = ele_ser.loc['registration_from'].values[0]
        from_obj.year_drop_down.value = temp_b[0: 4]
        j = 5
        month_val1 = ''
        for i in temp_b[5:]:
            j += 1
            if i != '/':
                month_val1 += i
            else:
                break
        from_obj.months_drop_down.value = month_val1
        from_obj.days_drop_down.value = temp_b[j:]

    if pd.isna(ele_ser.loc['registration_to'].values[0]) is False:
        temp_a = ele_ser.loc['registration_to'].values[0]
        to_obj.year_drop_down.value = temp_a[0: 4]
        month_val2 = ''
        k = 5
        for i in temp_a[5:]:
            k += 1
            if i != '/':
                month_val2 += i
            else:
                break
        to_obj.months_drop_down.value = month_val2
        to_obj.days_drop_down.value = temp_a[k:]

    alertdialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            value="Registration Date",
            size=25,
        ),
        content=ft.Column(
            [
                ft.Column(
                    [
                        ft.Text(
                            value="From:",
                            size=20,
                        ),
                        ft.Row(
                            [
                                from_obj.year_drop_down,
                                from_obj.months_drop_down,
                                from_obj.days_drop_down
                            ]
                        )
                    ],
                ),
                ft.Column(
                    [
                        ft.Text(
                            value="To:",
                            size=20,
                        ),
                        ft.Row(
                            [
                                to_obj.year_drop_down,
                                to_obj.months_drop_down,
                                to_obj.days_drop_down
                            ]
                        )
                    ],
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            height=230,
            width=400,
        ),
        actions=[
            ft.TextButton(
                text="Save",
                on_click=save_on_click,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = alertdialog
    alertdialog.open = True
    page.update()
