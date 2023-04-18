from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import datetime
from bson import ObjectId
from tools import selected_gyms, selected_type_gyms
from work_with_bd import send_trainer_for_query, take_working_schedule, get_gyms, get_user_gyms

stack = []

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton(text='Удалить_запись')
b2 = KeyboardButton(text='Записаться')
kb_menu.add(b2, b1)


def create_start_menu():
    """
        Функция для создания клавиатуры с залами,
        проверка для того что бы добавлять галочки если второе произошло нажатие
    """
    gyms = get_gyms()
    gyms_button = []
    for gym in gyms:
        gym_title = gym['title']
        if gym_title in selected_gyms:
            gym_title = "✅ " + gym_title
        gyms_button.append(InlineKeyboardButton(text=gym_title, callback_data=f'gym_{gym_title}'))
    gyms_button.append(InlineKeyboardButton(text='Дальше', callback_data=f'next'))
    ikb_choice_gym = InlineKeyboardMarkup(row_width=1)
    ikb_choice_gym.add(*gyms_button)
    stack.append(ikb_choice_gym)
    return ikb_choice_gym


def create_additional_mian_choice_menu(telegram_id):
    """
       Функция для создания клавиатуры в которой можно выбрать основные залы,
       проверка для того что бы добавлять галочки если второе произошло нажатие
   """
    user_gyms = get_user_gyms(telegram_id)
    buttons = []
    for ug in user_gyms:
        title = ug['id_gym']
        if title in selected_type_gyms:
            title = "основной " + ug['id_gym']
        buttons.append(InlineKeyboardButton(text=title, callback_data=f'choice_{title}'))
    buttons.append(InlineKeyboardButton(text='Дальше', callback_data='next_step'))
    ik_choice_additional_main = InlineKeyboardMarkup(row_width=1)
    ik_choice_additional_main.add(*buttons)
    return ik_choice_additional_main


def create_calendar_if_not_work_schedule(week_days, today, trainer, tr_id, holiday_days):
    """
        Функция для создания календаря если нету рабочего графика
    :param week_days: дни недели
    :param today: сегодня
    :param trainer: тренер
    :param tr_id: тренер ID
    :param holiday_days: выходные дни
    """
    buttons = []
    ikb = InlineKeyboardMarkup(row_width=7)

    for day in week_days:
        buttons.append(InlineKeyboardButton(text=day, callback_data=f'day_week_{day}'))
    ikb.row(*buttons)

    row = []
    for week in range(4):
        for day in week_days:
            button_text = today.strftime('%d')
            week_button_text = today.strftime('%d.%m')
            if today.strftime('%a') == str(day):
                comparison = today.strftime('%d.%m')
                if comparison not in holiday_days:
                    row.append(InlineKeyboardButton(text=f'{button_text}',
                                                    callback_data=f'record_{today.strftime("%d.%m.%y")}_{tr_id}'))
                else:
                    row.append(InlineKeyboardButton(text='🚫', callback_data=f'week_{week_button_text}_{trainer}'))
                today += datetime.timedelta(days=1)
            else:
                row.append(InlineKeyboardButton(text=' ', callback_data='ignore'))
    ikb.add(*row)
    ikb.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    stack.append(ikb)
    return ikb


def create_calendar_work_schedule(tr_id, week_days, today):
    """
        Функция длс создания календаря по рабочему графику
    :param tr_id: тренер ID
    :param week_days: дни недели
    :param today: сегодня
    """
    query = {'_id': ObjectId(tr_id)}
    trainer = send_trainer_for_query(query)
    data_lst = []
    for tr_data in trainer['working_schedule']['work_days']:
        data_lst.append(tr_data['date'])
    ikb = InlineKeyboardMarkup()

    # data_lst = ['05.04', '06.04', '07.04', '08.04', '09.04']
    # buttons = []
    # for _day in week_days:
    #     buttons.append(InlineKeyboardButton(text=_day, callback_data=f'day_week_{_day}'))
    # ikb.row(*buttons)
    buttons = []
    for day in data_lst:
        buttons.append(InlineKeyboardButton(text=day, callback_data=f'record_{day}_{tr_id}'))
    ikb.add(*buttons)
    ikb.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    stack.append(ikb)
    return ikb



