import random
import flet as ft

temp_code = None


def code_generate(page: ft.Page):
    global temp_code
    temp_code = str(random.randrange(1000, 99999))
    page.set_clipboard(temp_code)


def code_checker(value):
    global temp_code
    if value == temp_code:
        return True
    else:
        return False
