import locale

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from bd import *

stack = []


def create_start_menu():
    """
        Функция для создания стартового меню
    """
    kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='Записаться')
    # b2 = KeyboardButton(text='Удалить запись')
    b4 = KeyboardButton(text='Показать мои записи')
    return kb_menu.add(b1).add(b4)


def create_first_menu(telegram_id):
    """
        Функция для создания клавиатуры с залами,
        проверка для того что бы добавлять галочки если второе произошло нажатие
    """
    gyms = get_gyms()
    gyms_button = []
    for gym in gyms:
        gym_id = gym['_id']
        title = f"[-] {gym['title']}"
        gym_title = gym['title']
        if str(gym_id) in selected_gyms(telegram_id):
            title = f'[+] {title.split(" ")[1]}'
        gyms_button.append(InlineKeyboardButton(text=title, callback_data=f'gym_{gym_title}_{gym_id}'))
    gyms_button.append(InlineKeyboardButton(text='Готово', callback_data=f'first_step'))
    ikb_choice_gym = InlineKeyboardMarkup(row_width=1)
    ikb_choice_gym.add(*gyms_button)
    # stack.append(ikb_choice_gym)
    return ikb_choice_gym


def create_additional_mian_choice_menu(telegram_id):
    """
       Функция для создания клавиатуры в которой можно выбрать основные залы,
       проверка для того что бы добавлять галочки если второе произошло нажатие
   """
    user_gyms = get_user_gyms(telegram_id)
    buttons = []
    for ug in user_gyms:
        title = f'[{ug["status_gym"]}] {ug["gym"]}'
        buttons.append(InlineKeyboardButton(text=title, callback_data=f'choice_{title}'))
    buttons.append(InlineKeyboardButton(text='Готово', callback_data='second_step'))
    ik_choice_additional_main = InlineKeyboardMarkup(row_width=1)
    ik_choice_additional_main.add(*buttons)
    return ik_choice_additional_main


def create_choice_gym(telegram_id):
    """
       Функция для создания отображения основных и дополнительных залов
    """
    gyms = get_user_gyms(telegram_id)
    main = []
    extra = []
    for gym in gyms:
        title = f"[{gym['status_gym']}] {gym['gym']}"
        if gym['status_gym'] == 'основной':
            main.append(InlineKeyboardButton(text=title, callback_data=f'ch_gym_{title}'))
        else:
            extra.append(InlineKeyboardButton(text=title, callback_data=f'ch_gym_{title}'))
    extra.append(InlineKeyboardButton(text='Изменить привязанные залы', callback_data=f'cho_gym'))
    ikb = InlineKeyboardMarkup(row_width=1)
    buttons = main + extra
    ikb.add(*buttons)
    stack.append(ikb)
    return ikb


def create_choice_trainers_menu(gym, telegram_id):
    """
        Функция для создания меню с тренерами
    """
    trainers_in_gym = get_trainers_in_gym(gym)
    trainers = get_trainers(trainers_in_gym)
    buttons = []
    for trainer in trainers:
        trainer_id = trainer['_id']
        title = f"[-] {trainer['name']} {trainer['last_name']}"
        if str(trainer_id) in selected_trainers(telegram_id):
            title = f'[+] {" ".join(title.split(" ")[1:])}'
        buttons.append(InlineKeyboardButton(text=title, callback_data=f'tr_{gym}_{trainer_id}'))
    buttons.append(InlineKeyboardButton(text='Сохранить тренеров', callback_data=f'save_trainer_{gym}'))
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(*buttons)
    return ikb


def send_menu_with_trainer(telegram_id, gym):
    """
        Функция для вывода привязанных тренеров
    """
    trainers_id = get_trainers_id(telegram_id, gym)
    trainers = get_user_trainers(trainers_id)

    buttons = []
    # в trainer у нас вся информация по тренеру из бд
    for trainer in trainers:
        tr_id = trainer['_id']
        name = trainer['name']
        last_name = trainer['last_name']
        full_name = f'{name} {last_name}'
        buttons.append(InlineKeyboardButton(text=full_name, callback_data=f'trainer_{full_name}_{tr_id}'))

    buttons.append(
        InlineKeyboardButton(text='Изменить привязанных к этому залу тренеров', callback_data=f'change_{gym}'))
    buttons.append(
        InlineKeyboardButton(text='Назад', callback_data=f'back'))

    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(*buttons)
    stack.append(ikb)
    return ikb


def create_calendar(trainer_id):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    work_days = get_work_days(trainer_id)
    ikb = InlineKeyboardMarkup(row_width=7)
    week_days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    today = datetime.datetime.today()

    week_buttons = []
    for week_day in week_days:
        week_buttons.append(InlineKeyboardButton(text=week_day, callback_data=f'week_day_{week_day}'))
    ikb.row(*week_buttons)

    buttons = []
    # тут мы жестко задали 4 недели, можно попробовать сделать:
    # выводить даты до конца нашего списка (start-текущий день, end-последний день из нашего списка из work_days)

    for week in range(4):
        for week_day in week_days:
            button_text = today.strftime('%d.%m')
            if today.strftime('%a') == str(week_day):
                if today.strftime('%d.%m') in work_days:
                    buttons.append(
                        InlineKeyboardButton(text=button_text, callback_data=f'day_{button_text}_{trainer_id}'))
                else:
                    buttons.append(InlineKeyboardButton(text='...', callback_data='not_data_in_db'))
                today += datetime.timedelta(days=1)
            else:
                buttons.append(InlineKeyboardButton(text=' ', callback_data='past_days'))

    ikb.add(*buttons)
    ikb.row(InlineKeyboardButton(text='Назад', callback_data='back'))
    stack.append(ikb)
    return ikb


def time_menu(trainer_id, day):
    """
        Функция создает меню с рабочим временем тренера
    """
    trainer_work_time, trainer_name, trainer_last_name = get_trainer_work_time(trainer_id, day)
    start = int(trainer_work_time.split('-')[0])
    end = int(trainer_work_time.split('-')[1])
    text_message = f'Выберите время для записи к {trainer_name} {trainer_last_name} на {day}:'
    buttons = []
    for hour in range(start, end):
        start_time = f'{hour:02d}:00'
        end_time = f'{hour + 1:02d}:00'
        if start_time != check_time(trainer_id, day):
            button_text = f'{start_time} - {end_time}'
            buttons.append(
                InlineKeyboardButton(text=button_text, callback_data=f'finish_{day}_{trainer_id}_{button_text}'))
    ikb = InlineKeyboardMarkup()
    ikb.add(*buttons)
    ikb.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    stack.append(ikb)
    return ikb, text_message


def record_menu(telegram_id):
    records = send_user_record(telegram_id)
    buttons = []
    for record in records:
        trainer_id = record['trainer_id']
        trainer_name = f"{record['trainer_name']} {record['trainer_last_name']}"
        if str(trainer_id) in selected_del_record(telegram_id):
            trainer_name = "✅ " + f"{record['trainer_name']} {record['trainer_last_name']}"
        time = str(record['time'])
        date = record['date']
        buttons.append(
            InlineKeyboardButton(text=f'{trainer_name} {date} с {time.split("-")[0]} до {time.split("-")[1]}',
                                 callback_data=f't_del_{trainer_id}'))

    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(*buttons)
    ikb.add(InlineKeyboardButton(text='УДАЛИТЬ ЗАПИСЬ', callback_data=f'delete_'))
    ikb.add(InlineKeyboardButton(text='Назад', callback_data='_back'))
    return ikb
