selected_type_gyms = set()


def delete_excess_click_in_additional_main_menu(selected_type_gym):
    """
        Функция для удаления ненужного клика(без нее при нажатии будет лишний клик)
    :param selected_type_gym: выбранный зал
    """
    for selected_type in selected_type_gyms.copy():
        if selected_type != selected_type_gym and selected_type in selected_type_gym:
            return selected_type_gyms.remove(selected_type)
