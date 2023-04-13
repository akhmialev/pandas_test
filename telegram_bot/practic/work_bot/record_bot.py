import locale

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from config import TOKEN

from work_with_bd import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_activiti_day = {}
stack = []


async def on_startup(_):
    print('Бот включен')


def create_calendar_if_not_work_schedule(week_days, today, trainer, tr_id, holiday_days):
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


@dp.message_handler(commands='start')
async def menu(msg: types.Message):
    """
    Функция создает стартовое меню
    """
    user_id = msg.from_user.id
    username = msg.from_user.username
    first_name = msg.from_user.first_name
    create_user_in_db(user_id, username, first_name)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton(text='Удалить_запись')
    b2 = KeyboardButton(text='Записаться')
    kb.add(b2, b1)
    await bot.send_message(chat_id=msg.from_user.id, text='Сделайте выбор', reply_markup=kb)


@dp.message_handler()
async def send_choice_all_trainers(msg: types.Message):
    """
    Функция вывода выбора тренеров
    """
    if 'записаться' in msg.text.lower():
        # Нее разобрался почему не работает с русским в 125 строчке callback_data
        trainers_button = []
        trainers = send_all_trainers()

        for element in trainers:
            name = element['name']
            last_name = element['last_name']
            tr_id = element['_id']
            fullname = name + ' ' + last_name
            button = InlineKeyboardButton(text=fullname, callback_data=f'trainer_{fullname}_{tr_id}')
            trainers_button.append(button)
        ikb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        ikb.add(*trainers_button)
        stack.append(ikb)
        # print(stack)
        await bot.send_message(chat_id=msg.from_user.id, text='Выберите тренера', reply_markup=ikb)
    else:
        """
            здесь код для удаления записи
        """


@dp.callback_query_handler(lambda c: c.data.startswith('ignore'))
async def calendar_empty_days(cb: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=cb.id)


@dp.callback_query_handler(lambda c: c.data.startswith('day_week_'))
async def calendar_days_click(cb: types.CallbackQuery):
    """
    Функция для отображения полного названия месяца при клике в календаре на месяц
    """
    day = cb.data.split('_')[2]
    days_dct = {
        'пн': 'Понедельник',
        'вт': 'Вторник',
        'ср': 'Среда',
        'чт': 'Четверг',
        'пт': 'Пятница',
        'сб': 'Суббота',
        'вс': 'Воскресение',

    }
    if str(day) in days_dct:
        await bot.answer_callback_query(callback_query_id=cb.id, text=f'{days_dct[str(day)]}')


@dp.callback_query_handler(lambda c: c.data.startswith('trainer_'))
async def calendar_record_trainers(cb: types.CallbackQuery):
    """
    Функция выводит рабочие даты тренера.
    """
    trainer = cb.data.split('_')[1]
    tr_id = cb.data.split('_')[2]
    calendar_msg = f'Выберете дату занятия с {trainer}: '
    calendar_markup = create_calendar(trainer, tr_id)
    await bot.edit_message_text(chat_id=cb.from_user.id, text=calendar_msg, message_id=cb.message.message_id,
                                reply_markup=calendar_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('record_'))
async def send_time_for_record(cb: types.CallbackQuery):
    """
    Функция выводит меню времени для записи
    """
    list_data = cb.data.split('_')
    date = list_data[1]
    tr_id = list_data[2]
    name, last_name = take_trainer_name(tr_id)
    trainer = get_work_time(tr_id, date)
    start_time = int(trainer.split('-')[0])
    end_time = int(trainer.split('-')[1])
    text_message = f'Выберите время для записи к {name} {last_name} на {date}:'
    ikb = InlineKeyboardMarkup()
    buttons = []
    for hour in range(start_time, end_time):
        start_time = f'{hour:02d}:00'
        end_time = f'{hour + 1:02d}:00'
        if start_time != check_time(tr_id, date):
            training_time = f'{start_time} - {end_time}'
            buttons.append(
                InlineKeyboardButton(text=training_time, callback_data=f'finish_{date}_{training_time}_{tr_id}'))
    ikb.add(*buttons)
    ikb.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    stack.append(ikb)
    await bot.answer_callback_query(callback_query_id=cb.id)
    await bot.edit_message_text(chat_id=cb.from_user.id, text=text_message, message_id=cb.message.message_id,
                                reply_markup=ikb)


@dp.callback_query_handler(lambda c: c.data.startswith('week_'))
async def send_record_time_week_day(cb: types.CallbackQuery):
    """
    Функция для отображения текста если пытаются записаться на выходной день
    """
    list_data = cb.data.split('_')
    status = list_data[0]
    week_day = list_data[1]
    trainer = list_data[2]

    if status == 'week':
        await bot.answer_callback_query(callback_query_id=cb.id, text=f'У {trainer} {week_day} не рабочий день')


@dp.callback_query_handler(lambda c: c.data.startswith('finish_'))
async def finish_record_and_add_to_db(cd: types.CallbackQuery):
    """
    Функция делает запись на определенное время и делает проверку, записаться можно только раз в день
    """
    telegram_id = str(cd.from_user.id)
    record_date = cd.data.split('_')[1]
    record_time = cd.data.split('_')[2]
    tr_id = str(cd.data.split('_')[3])

    if check_user_click(telegram_id, tr_id):
        await bot.send_message(chat_id=cd.from_user.id, text='Вы уже записаны')
    else:
        list_data = cd.data.split('_')
        training_time = list_data[2]
        training_date = list_data[1]
        text_message = f'Вы записаны {training_date}  на время {training_time}'
        await bot.answer_callback_query(callback_query_id=cd.id)
        await bot.send_message(chat_id=cd.from_user.id, text=text_message)

        data_to_save = {
            'telegram_id': telegram_id,
            'first_name': cd['from']['first_name'],
            'username': cd['from']['username'],
            'record_date': record_date,
            'record_time': record_time,
            'date': str(datetime.datetime.now().date())
        }
        save_record_to_trainer(telegram_id, record_date, record_time, tr_id)
        save_user_click(data_to_save, tr_id)


@dp.callback_query_handler(lambda c: c.data.startswith('back'))
async def go_back(cb: types.CallbackQuery):
    """
        Функция кнопки назад
    """
    if len(stack) > 0:
        stack.pop()
        kb = stack[-1]
        await bot.answer_callback_query(callback_query_id=cb.id)
        await bot.edit_message_text(chat_id=cb.from_user.id, reply_markup=kb, message_id=cb.message.message_id,
                                    text='Вы вернулись в назад')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
