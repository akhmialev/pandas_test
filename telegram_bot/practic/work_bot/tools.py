import locale
import datetime
from keyboard import create_calendar_work_schedule
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


def create_calendar(trainer, tr_id):
    """
    Функция создает календарь с текущим днем плюс 4 недели, так же учитывает выходные дни тренера,
     ставит вместо даты стикер.
    :param trainer: имя фамилия тренера.
    :param tr_id: id тренера из базы данных.
    """
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    holiday_days = get_holiday_date(tr_id)
    week_days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    today = datetime.datetime.today()

    check_work_schedule = take_working_schedule(tr_id)
    # if check_work_schedule <= 27:
    #     return create_calendar_if_not_work_schedule(week_days, today, trainer, tr_id, holiday_days)
    # else:
    return create_calendar_work_schedule(tr_id, week_days, today)


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
