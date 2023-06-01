def menu_container_animation(container_var):
    container_var.width = 480 if container_var.width == 700 else 700
    container_var.height = 500 if container_var.height == 450 else 450
    container_var.update()


def register_container_animation(container_var):
    container_var.width = 850 if container_var.width == 700 else 700
    container_var.height = 550 if container_var.height == 450 else 450
    container_var.update()
