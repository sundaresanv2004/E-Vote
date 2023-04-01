def menu_container_animation(container_var) -> str:
    container_var.width = 480 if container_var.width == 700 else 700
    container_var.height = 500 if container_var.height == 450 else 450
    container_var.update()


def register_container_animation(container_var) -> str:
    pass


def settings_election_options_animation(container_var) -> str:
    container_var.height = 250 if container_var.height == 45 else 45
    container_var.update()


def settings_user_options_animation(container_var) -> str:
    container_var.height = 350 if container_var.height == 45 else 45
    container_var.update()


def settings_admin_options_animation(container_var) -> str:
    container_var.height = 350 if container_var.height == 45 else 45
    container_var.update()
