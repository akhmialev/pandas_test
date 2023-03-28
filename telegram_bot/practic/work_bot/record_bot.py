import datetime
import locale

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, CallbackGame
from test_data import trainers, TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print("Бот включен")


def record_to_db(dct):
    print(dct)


def create_dct_for_db(date):
    """
    Функция для формированья словаря, что бы записывать в БД
    :param date: данные для записи
        trainer - имя и фамилия терена
        training_time - время записи клиента
        training_date - дата записи клиента
    """
    trainer, training_time, training_date = date
    trainer = trainer.split(' ')
    training_date = '.'.join(training_date.split('.')[1:])
    dct = {
        'name': trainer[0],
        'lname': trainer[1],
        'time': training_time,
        'training_date': training_date

    }
    record_to_db(dct)


def get_mount_right_case():
    """
    Функция ставит месяц в именительный падеж
    """
    mount = ['Январе', 'Феврале', 'Марте', 'Апреле', 'Мае', 'Июне', 'Июле', 'Августе', 'Сентябре', 'Октябре', 'Ноябре',
             'Декабре']

    now = datetime.datetime.now()
    mount = mount[now.month - 1]
    return now, mount


def get_week_date(tr_id):
    """
    Функция берет список выходных дат тренера по его id
    :param tr_id: id тренера
    :return: возвращает список выходных дат
    """
    for trainer in trainers:
        if trainer['id'] == int(tr_id):
            return trainer['week_day']


user_activiti_day = {}


@dp.message_handler(commands='start')
async def menu(msg: types.Message):
    """
    Функция создает стартовое меню
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='Удалить_запись')
    b2 = KeyboardButton(text='Записаться')
    kb.add(b2, b1)
    await bot.send_message(chat_id=msg.from_user.id, text='Сделайте выбор', reply_markup=kb)


@dp.message_handler()
async def send_choice_all_trainers(msg: types.Message):
    """
    Функция вывода выбора тренеров
    :param msg:
    :return:
    """
    if 'записаться' in msg.text.lower():
        # здесь должно быть подключение к бд и вывод всех тренеров(я пока использовал просто список trainers с dict)
        trainers_button = []
        for element in trainers:
            name = element['name']
            lname = element['lname']
            tr_id = element['id']
            fullname = name + ' ' + lname
            button = InlineKeyboardButton(text=fullname, callback_data=f"trainer_{fullname}_{tr_id}")
            trainers_button.append(button)
        ikb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        ikb.add(*trainers_button)
        await bot.send_message(chat_id=msg.from_user.id, text='Выберите тренера', reply_markup=ikb)
    else:
        """
            здесь код для удаления записи
        """


@dp.callback_query_handler(lambda c: c.data.startswith('trainer_'))
async def calendar_record_trainers(cb: types.CallbackQuery):
    """
    Функция выводит рабочие даты тренера.
    :param cb: coll back дата тут приходит название объекта(терена), мы забираем из БД его рабочие дни и выводим
    Вывод текущий день + 28 дней
    """

    # тут просто формирую календарь на текущий день + 4 недели вперед с проверкой на выходные дни
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    trainer = cb.data.split('_')[1]
    tr_id = cb.data.split('_')[2]
    calendar_msg = f"Выберете дату занятия с {trainer}:"

    today = datetime.datetime.today()
    end_data = today + datetime.timedelta(days=28)
    week_days = get_week_date(tr_id)
    buttons = []
    while today <= end_data:
        comparison = today.strftime('%d.%m')
        button_text = today.strftime('%a %d.%m')
        if comparison not in week_days:
            buttons.append(InlineKeyboardButton(text=button_text,
                                                callback_data=f'record_{today.strftime("%d.%m.%y")}_{trainer}'))
        else:
            buttons.append(InlineKeyboardButton(text='🚫',
                                                callback_data=f'week_{button_text}_{trainer}'))
        today += datetime.timedelta(days=1)

    ikb = InlineKeyboardMarkup(row_width=4)
    ikb.add(*buttons)
    await bot.send_message(chat_id=cb.from_user.id, text=calendar_msg, reply_markup=ikb)


@dp.callback_query_handler(lambda c: c.data.startswith('record_'))
async def send_time_for_record(cb: types.CallbackQuery):
    """
    Функция выводит меню времени для записи
    """
    list_data = cb.data.split('_')
    date = list_data[1]
    trainer = list_data[2]

    text_message = f'Выберите время для записи к {trainer}:'
    ikb = InlineKeyboardMarkup()
    buttons = []
    for hour in range(7, 24):
        start_time = f'{hour:02d}:00'
        end_time = f'{hour + 1:02d}:00'
        training_time = f"{start_time} - {end_time}"
        buttons.append(
            InlineKeyboardButton(text=training_time, callback_data=f'finish record_{date}_{training_time}_{trainer}'))
    ikb.add(*buttons)

    await bot.send_message(chat_id=cb.from_user.id, text=text_message, reply_markup=ikb)


@dp.callback_query_handler(lambda c: c.data.startswith('finish '))
async def finish_record_and_add_to_db(cd: types.CallbackQuery):
    """
    Функция делает запись на определенное время и делает проверку, записаться можно только раз в день
    """
    user_id = cd.from_user.id
    if user_id in user_activiti_day and user_activiti_day[user_id] == datetime.datetime.now().date():
        await bot.send_message(chat_id=cd.from_user.id, text='Вы уже записаны')

    list_data = cd.data.split('_')
    trainer = list_data[3]
    training_time = list_data[2]
    training_date = list_data[1]
    text_message = f'Вы записаны {training_date} к тренеру {trainer} на время {training_time}'

    await bot.send_message(chat_id=cd.from_user.id, text=text_message)
    user_activiti_day[user_id] = datetime.datetime.now().date()
    print(user_activiti_day)
    data = trainer, training_time, training_date
    create_dct_for_db(data)


@dp.callback_query_handler(lambda c: c.data.startswith('week_'))
async def send_record_time(cb: types.CallbackQuery):
    """
    Функция для отображения текста если пытаются записаться на выходной день
    """
    list_data = cb.data.split('_')
    status = list_data[0]
    week_day = list_data[1]
    trainer = list_data[2]

    if status == 'week':
        await bot.answer_callback_query(callback_query_id=cb.id, text=f'У {trainer} {week_day} не рабочий день')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
