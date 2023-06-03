from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters import Text

from keyboards import *
from config import TOKEN
from bd import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот включен')


@dp.message_handler(commands=['start'])
async def start_bot(msg: types.Message):
    """
        Функция для активации бота, она проверяет есть ли пользователь в системе если есть то выводит меню для записи,
        если нет, то создает юзера и затем выводит меню для добавления параметров.
    """
    telegram_id = msg.from_user.id
    username = msg.from_user.username
    first_name = msg.from_user.first_name
    # проверка есть ли юзер в нашей бд
    if user_in_db(telegram_id):
        menu_st = create_start_menu()
        await bot.send_message(chat_id=msg.from_user.id, text='Стартовое меню', reply_markup=menu_st)

    else:
        create_user_in_db(telegram_id, username, first_name)
        menu_fr = create_first_menu(telegram_id)
        await bot.send_message(chat_id=msg.from_user.id, text='Выберите залы', reply_markup=menu_fr)


@dp.callback_query_handler(lambda cb: cb.data.startswith('gym_'))
async def click_start_menu(cb: types.CallbackQuery):
    """
        Обработчик нажатия кнопок в меню для выбора залов
    """
    selected_gym = cb.data.split('_')[1]
    telegram_id = cb.from_user.id
    gym_id = cb.data.split('_')[-1]

    if str(gym_id) in selected_gyms(telegram_id):
        await bot.answer_callback_query(callback_query_id=cb.id)
        delete_user_choice(telegram_id, selected_gym)
        delete_selected_trs(telegram_id, gym_id)
        delete_selected_gyms(gym_id, telegram_id)
    else:
        await bot.answer_callback_query(callback_query_id=cb.id)
        add_selected_gyms(gym_id, telegram_id)
        save_user_choice(telegram_id, selected_gym)
    keyboard = create_first_menu(telegram_id)
    try:
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=keyboard)
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda cb: cb.data.startswith('first_step'))
async def click_next_in_start_menu(cb: types.CallbackQuery):
    """
        Обработчик кнопки дальше
    """
    telegram_id = cb.from_user.id
    menu_kb = create_additional_mian_choice_menu(telegram_id)
    await bot.answer_callback_query(callback_query_id=cb.id)
    await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id, reply_markup=menu_kb,
                                text="Выберите основные залы")


@dp.callback_query_handler(lambda cb: cb.data.startswith('choice_'))
async def click_choice_additional_main(cb: types.CallbackQuery):
    """
        Обработчик нажатия кнопок меню для выбора основных залов
    """
    selected_type_gym = cb.data.split("_")[1]
    gym = selected_type_gym.split(' ')[1]
    telegram_id = cb.from_user.id
    status = (cb.data.split('_')[1]).split(' ')[0].strip('[').strip(']')
    if status == 'дополнительный':
        await bot.answer_callback_query(callback_query_id=cb.id)
        overwrite_main_status(telegram_id, gym)
    else:
        await bot.answer_callback_query(callback_query_id=cb.id)
        overwrite_extra_status(telegram_id, gym)

    keyboard = create_additional_mian_choice_menu(telegram_id)
    try:
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=keyboard)
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda cb: cb.data.startswith('status'))
async def change_status_gym(cb: types.CallbackQuery):
    telegram_id = cb.from_user.id
    keyboard = create_additional_mian_choice_menu(telegram_id)
    await bot.answer_callback_query(callback_query_id=cb.id)
    await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id, text='Выберите статус зала',
                                reply_markup=keyboard)


@dp.callback_query_handler(lambda cb: cb.data.startswith('second_step'))
async def next_step_menu(cb: types.CallbackQuery):
    """
        Функция для вывода для создания меню,
        когда пользователь выбрал основные/дополнительные залы, выводит стартовое меню
    """
    telegram_id = cb.from_user.id
    menu_kb = create_choice_gym(telegram_id)
    await bot.answer_callback_query(callback_query_id=cb.id)
    await bot.send_message(chat_id=cb.from_user.id, reply_markup=menu_kb, text='Стартовое меню')
    await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                        reply_markup=InlineKeyboardMarkup())


@dp.message_handler(Text(equals='Записаться'))
async def choice_in_start_menu(msg: types.Message):
    """
        Функция обработчик кнопки 'записаться', если у пользователя есть выбранные залы в бд то пойдем по ветке записи,
        если нет залов в бд, пойдем по ветке добавления залов в бд
    """
    telegram_id = msg.from_user.id
    menu_fr = create_first_menu(telegram_id)
    if user_have_gym(telegram_id):
        menu_choice_gym = create_choice_gym(telegram_id)
        await bot.send_message(chat_id=msg.from_user.id, text='Выберите зал', reply_markup=menu_choice_gym)

    else:
        await bot.send_message(chat_id=msg.from_user.id, text='Выберите зал', reply_markup=menu_fr)


@dp.callback_query_handler(lambda cb: cb.data.startswith('cho_gym'))
async def change_choice_gym(cb: types.CallbackQuery):
    """
        Функция выводит залы пользователя из бд для последующей записи
    """
    telegram_id = cb.from_user.id
    await bot.answer_callback_query(callback_query_id=cb.id)
    menu_fr = create_first_menu(telegram_id)
    await bot.send_message(chat_id=cb.from_user.id, text='Выберите зал', reply_markup=menu_fr)
    await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                        reply_markup=InlineKeyboardMarkup())


@dp.callback_query_handler(lambda cb: cb.data.startswith('ch_'))
async def choice_gym(cb: types.CallbackQuery):
    """
        Функция для вывода тренеров пользователя,
        если у него есть уже тренера в бд то выведет их, если нет предложить выбрать
    """
    telegram_id = cb.from_user.id
    gym = cb.data.split(' ')[1]
    if trainers_in_user(telegram_id, gym):
        await bot.answer_callback_query(callback_query_id=cb.id)
        menu_trainers = send_menu_with_trainer(telegram_id, gym)
        await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                    text='Выбор тренера для записи', reply_markup=menu_trainers)
    else:
        await bot.answer_callback_query(callback_query_id=cb.id)
        menu_tr = create_choice_trainers_menu(gym, telegram_id)
        await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id, text='Выберите тренеров',
                                    reply_markup=menu_tr)


@dp.callback_query_handler(lambda cb: cb.data.startswith('tr_'))
async def choice_trainer(cb: types.CallbackQuery):
    """
        Функция обрабатывает выбор пользователя и записывает в бд
    """
    gym = cb.data.split('_')[1]
    trainer_id = cb.data.split('_')[-1]
    data = cb.data
    telegram_id = cb.from_user.id

    if str(trainer_id) in selected_trainers(telegram_id):
        await bot.answer_callback_query(callback_query_id=cb.id)
        delete_selected_trainers(telegram_id, trainer_id)
        delete_trainer_in_user(data, telegram_id)
    else:
        await bot.answer_callback_query(callback_query_id=cb.id)
        add_selected_trainers(telegram_id, trainer_id)
        save_trainer_in_user(data, telegram_id)
    keyboard = create_choice_trainers_menu(gym, telegram_id)
    try:
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=keyboard)
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda cb: cb.data.startswith('save_trainer'))
async def save_trainer(cb: types.CallbackQuery):
    """
        Функция для обработки кнопки 'Сохранить тренеров', просто выводит следующее меню
    """
    telegram_id = cb.from_user.id
    gym = cb.data.split('_')[-1]
    if not selected_trainers(telegram_id):
        await bot.answer_callback_query(callback_query_id=cb.id, text='Вы не выбрали ни одного тренера')
    else:
        await bot.answer_callback_query(callback_query_id=cb.id)
        menu_trainers = send_menu_with_trainer(telegram_id, gym)
        await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                    text='Выбор тренера для записи', reply_markup=menu_trainers)


@dp.callback_query_handler(lambda cb: cb.data.startswith('change'))
async def change_trainer(cb: types.CallbackQuery):
    """
        Функция для обработки кнопки 'Изменить привязанных к этому залу тренеров', возвращает меню со всеми тренерами
    """
    telegram_id = cb.from_user.id
    gym = cb.data.split('_')[-1]
    await bot.answer_callback_query(callback_query_id=cb.id)
    menu_tr = create_choice_trainers_menu(gym, telegram_id)
    await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id, reply_markup=menu_tr)


@dp.callback_query_handler(lambda cb: cb.data.startswith('trainer_'))
async def trainer_date_output(cb: types.CallbackQuery):
    """
        Функция создает календарь из рабочего графика выбранного тренера
    """
    trainer_id = cb.data.split('_')[-1]
    trainer_name = cb.data.split('_')[1]
    menu_kb = create_calendar(trainer_id)
    await bot.answer_callback_query(callback_query_id=cb.id)
    await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                text=f'Выберите дату для записи к тренеру {trainer_name}', reply_markup=menu_kb)


@dp.callback_query_handler(lambda cb: cb.data.startswith('week_'))
async def trainer_time_output(cb: types.CallbackQuery):
    """
        Функция для вывода полного дня неделе если пользователь нажмет на календаре
    """
    day = cb.data.split('_')[2]
    days = {
        'пн': 'Понедельник',
        'вт': 'Вторник',
        'ср': 'Среда',
        'чт': 'Четверг',
        'пт': 'Пятница',
        'сб': 'Суббота',
        'вс': 'Воскресение',

    }
    if str(day) in days:
        await bot.answer_callback_query(callback_query_id=cb.id, text=f'{days[day]}')


@dp.callback_query_handler(lambda cb: cb.data.startswith('not_data_in_db'))
async def not_data_in_db(cb: types.CallbackQuery):
    """
        Функция для вывода сообщения, если у тренера нет это даты в бд
    """
    await bot.answer_callback_query(callback_query_id=cb.id, text='Тренер на этот день не сделал расписание')


@dp.callback_query_handler(lambda cb: cb.data.startswith('past_days'))
async def past_days(cb: types.CallbackQuery):
    """
        Функция для вывода сообщения, если пользователь нажмет на прошедшую дату
    """
    await bot.answer_callback_query(callback_query_id=cb.id, text='Прошедший день')


@dp.callback_query_handler(lambda cb: cb.data.startswith('day'))
async def selected_day(cb: types.CallbackQuery):
    """
        Функция выводит меню с рабочим временем тренера
    """
    trainer_id = cb.data.split('_')[-1]
    day = cb.data.split('_')[1]
    menu_kb, text_message = time_menu(trainer_id, day)

    await bot.answer_callback_query(callback_query_id=cb.id)
    await bot.edit_message_text(chat_id=cb.from_user.id, text=text_message, message_id=cb.message.message_id,
                                reply_markup=menu_kb)


@dp.callback_query_handler(lambda cb: cb.data.startswith('finish'))
async def record_to_trainer(cb: types.CallbackQuery):
    """
        Функция проверяет записан ли пользователь на текущий день если нет, то записывает в бд,
        если да то выводит сообщение, что вы уже записаны
    """
    telegram_id = cb.from_user.id
    trainer_id = cb.data.split('_')[2]
    day = cb.data.split('_')[1]
    time = cb.data.split('_')[-1]
    first_name = cb.from_user.first_name
    username = cb.from_user.username
    menu_st = create_start_menu()

    trainer_name, trainer_last_name = get_user_name(trainer_id)
    text_message = f'Вы записаны к {trainer_name} {trainer_last_name} на {day}' \
                   f' c {time.split("-")[0]} до {time.split("-")[1]}'

    if check_user_click(telegram_id, trainer_id):
        await bot.answer_callback_query(callback_query_id=cb.id)
        await bot.send_message(chat_id=cb.from_user.id, text=f'Вы уже записаны к {trainer_name} {trainer_last_name} ')
        await bot.send_message(chat_id=cb.from_user.id, text='Стартовое меню', reply_markup=menu_st)
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=InlineKeyboardMarkup())
    else:
        save_record_to_trainer(telegram_id, trainer_id, time, day, first_name, username)
        save_record_to_user(telegram_id, trainer_id, time, day, trainer_name, trainer_last_name)
        save_user_click(telegram_id, trainer_id)

        await bot.answer_callback_query(callback_query_id=cb.id)
        await bot.send_message(chat_id=cb.from_user.id, text='Стартовое меню', reply_markup=menu_st)

        await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id, text=text_message,
                                    reply_markup=InlineKeyboardMarkup())


@dp.callback_query_handler(lambda c: c.data.startswith('back'))
async def button_back(cb: types.CallbackQuery):
    """
        Функция кнопки назад
    """
    if len(stack) > 0:
        stack.pop()
        kb = stack[-1]
        await bot.answer_callback_query(callback_query_id=cb.id)
        await bot.edit_message_text(chat_id=cb.from_user.id, reply_markup=kb, message_id=cb.message.message_id,
                                    text='Вы вернулись в назад')


@dp.message_handler(Text(equals='Показать мои записи'))
async def user_records(msg: types.Message):
    # надо добавить проверку что если нет записей то вывести ответ что у вас нет еще записей
    telegram_id = msg.from_user.id
    records = send_user_record(telegram_id)
    menu_st = create_start_menu()
    for record in records:
        trainer_name = f"{record['trainer_name']} {record['trainer_last_name']}"
        time = str(record['time'])
        date = record['date']
        await bot.send_message(chat_id=msg.from_user.id,
                               text=f'Вы записаны к {trainer_name} {date} с {time}')
    await bot.send_message(chat_id=msg.from_user.id, text='Стартовое меню', reply_markup=menu_st)


@dp.message_handler(Text(equals='Удалить запись'))
async def delete_record(msg: types.Message):
    """
        Функция для удаления записи
    """
    telegram_id = msg.from_user.id
    menu_record = record_menu(telegram_id)
    await bot.send_message(chat_id=msg.from_user.id, text='Выберите запись для удаления', reply_markup=menu_record)


@dp.message_handler(commands=['привязать', 'cancel'])
async def process_message(msg: types.Message):
    """
        Функция для меню которое привязывает к тг юзеру web юзера
    """
    if msg.text == '/привязать':
        await msg.reply('Введите ваш ID:')
    elif msg.text == '/cancel':
        await msg.reply('Привязка отменена')
    else:
        await msg.reply('Неизвестная команда')


@dp.message_handler()
async def bind_id(msg: types.Message):
    """
        Функция для меню для привязки юзера и вывода ответа
    """
    telegram_id = msg.from_user.id
    if len(msg.text) == 24:
        crm_id = msg.text
        if bind_user(telegram_id, crm_id):
            await bot.send_message(chat_id=msg.from_user.id, text='Вы успешно привязали ID')
        else:
            await bot.send_message(chat_id=msg.from_user.id, text='Ошибка, неправильный ID')


@dp.callback_query_handler(lambda cb: cb.data.startswith('_'))
async def button_back_in_delete_menu(cb: types.CallbackQuery):
    menu_st = create_start_menu()
    await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                        reply_markup=InlineKeyboardMarkup())
    await bot.send_message(chat_id=cb.from_user.id, text='Стартовое меню', reply_markup=menu_st)
    await bot.delete_message(chat_id=cb.from_user.id, message_id=cb.message.message_id)


@dp.callback_query_handler(lambda cb: cb.data.startswith('t_del'))
async def delete_records(cb: types.CallbackQuery):
    trainer_id = cb.data.split('_')[-1]
    telegram_id = cb.from_user.id
    if str(trainer_id) in selected_trainers(telegram_id):
        await bot.send_message(chat_id=cb.from_user.id, text='hi')
        delete_selected_records(telegram_id, trainer_id)
    else:
        await bot.send_message(chat_id=cb.from_user.id, text='no')
        add_selected_records(telegram_id, trainer_id)
    keyboard = record_menu(telegram_id)
    try:
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=keyboard)
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda cb: cb.data.startswith('delete_'))
async def delete_records(cb: types.CallbackQuery):
    await bot.send_message(chat_id=cb.from_user.id, text='hi')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
