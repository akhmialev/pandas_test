from work_with_bd import send_all_trainers, take_working_schedule

selected_gyms = set()
selected_type_gyms = set()


def delete_excess_click(selected_gym):
    """
    Функция для удаления ненужного клика(без нее при нажатии будет лишний клик)
    :param selected_gym: выбранный зал
    """
    for gym in selected_gyms.copy():
        if gym != selected_gym and gym in selected_gym:
            return selected_gyms.remove(gym)


def delete_excess_click_in_additional_main_menu(selected_type_gym):
    """
        Функция для удаления ненужного клика(без нее при нажатии будет лишний клик)
    :param selected_type_gym: выбранный зал
    """
    for selected_type in selected_type_gyms.copy():
        if selected_type != selected_type_gym and selected_type in selected_type_gym:
            return selected_type_gyms.remove(selected_type)





def get_holiday_date(tr_id):
    """
        Функция берет список выходных дат тренера по его id
    :param tr_id: id тренера
    :return: возвращает список выходных дат
    """
    trainers = send_all_trainers()

    for trainer in trainers:
        trainer_id = trainer['_id']
        if str(trainer_id) == tr_id:
            return trainer['working_schedule']['weekend_days']
