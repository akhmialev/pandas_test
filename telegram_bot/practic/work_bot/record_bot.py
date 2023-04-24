from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.exceptions import MessageNotModified

from config import TOKEN
from keyboard import *
from work_with_bd import *
from tools import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот включен')


@dp.message_handler(commands='start')
async def menu(msg: types.Message):
    """
        Функция вызова стартового меню
    """
    user_id = msg.from_user.id
    username = msg.from_user.username
    first_name = msg.from_user.first_name
    # не забудь поставить в if not для корректной работы
    if not check_user_in_db(user_id):
        create_user_in_db(user_id, username, first_name)
        keyboard = create_start_menu()
        await bot.send_message(chat_id=msg.from_user.id, text='Выберите тренажерные залы', reply_markup=keyboard)
    else:
        # pass
        menu_kb = create_record_del_record_menu()
        await bot.send_message(chat_id=msg.from_user.id, text='Сделайте выбор', reply_markup=menu_kb)


@dp.callback_query_handler(lambda cb: cb.data.startswith('next_step'))
async def next_step_menu(cb: types.CallbackQuery):
    menu_kb = create_record_del_record_menu()
    await bot.send_message(chat_id=cb.from_user.id, text='Сделайте выбор', reply_markup=menu_kb)
    await bot.edit_message_text(chat_id=cb.from_user.id, text='Основное меню', message_id=cb.message.message_id,
                                reply_markup=InlineKeyboardMarkup())


@dp.callback_query_handler(lambda cb: cb.data.startswith('gym_'))
async def click_start_menu(cb: types.CallbackQuery):
    """
        Обработчик нажатия кнопок в меню для выбора залов
    """
    selected_gym = cb.data.split('_')[1]
    telegram_id = cb.from_user.id
    if '✅ ' in cb.data.split('_')[1]:
        delete_user_choice(telegram_id, selected_gym.split(' ')[1])
    else:
        save_user_choice(telegram_id, selected_gym)

    if selected_gym in selected_gyms:
        delete_excess_click(selected_gym)
        selected_gyms.remove(selected_gym)
        await bot.answer_callback_query(callback_query_id=cb.id)

    else:
        selected_gyms.add(selected_gym)
        delete_excess_click(selected_gym)
        await bot.answer_callback_query(callback_query_id=cb.id)
    keyboard = create_start_menu()
    try:
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=keyboard)
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda cb: cb.data.startswith('choice_'))
async def click_choice_additional_main(cd: types.CallbackQuery):
    """
        Обработчик нажатия кнопок меню для выбора основных залов
    """
    selected_type_gym = cd.data.split("_")[1]
    telegram_id = cd.from_user.id
    if 'основной ' not in (cd.data.split('_')[1]):
        save_user_data(telegram_id, selected_type_gym)
    else:
        selected_type_gym = selected_type_gym.split(' ')[1]
        delete_user_data(telegram_id, selected_type_gym)

    if selected_type_gym in selected_type_gyms:
        delete_excess_click_in_additional_main_menu(selected_type_gym)
        selected_type_gyms.remove(selected_type_gym)
        await bot.answer_callback_query(callback_query_id=cd.id)
    else:
        selected_type_gyms.add(selected_type_gym)
        delete_excess_click_in_additional_main_menu(selected_type_gym)
        await bot.answer_callback_query(callback_query_id=cd.id)
    keyboard = create_additional_mian_choice_menu(telegram_id)
    try:
        await bot.edit_message_reply_markup(chat_id=cd.from_user.id, message_id=cd.message.message_id,
                                            reply_markup=keyboard)
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda cb: cb.data.startswith('next'))
async def click_next_in_start_menu(cb: types.CallbackQuery):
    """
        Обработчик кнопки дальше
    """
    telegram_id = cb.from_user.id
    menu_kb = create_additional_mian_choice_menu(telegram_id)
    await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id, reply_markup=menu_kb,
                                text="Выберите основные залы")


@dp.message_handler()
# тут еще до вывода тренеров нужно выводить залы для того что бы человек выбрал зал, а потом из этого зала тренеров!!!
async def send_choice_all_trainers(msg: types.Message):
    """
        Функция вывода выбора тренеров
    """
    telegram_id = msg.from_user.id
    if 'записаться' in msg.text.lower():
        if check_user_trainer(telegram_id):
            menu_kb = send_gym_for_record(telegram_id)
            await bot.send_message(chat_id=msg.from_user.id, text='Выберите зал для добавления тренеров',
                                   reply_markup=menu_kb)
        # в else надо выводить уже тренеров записанных в бд юзера!!!
        else:
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


@dp.callback_query_handler(lambda cb: cb.data.startswith('recordgym'))
async def add_trainers_to_user(cb: types.CallbackQuery):
    """
        Создание меню для добавления тренеров
    """
    gym = cb.data.split('_')[1].split(' ')[0]
    trainers_id = get_id_trainers(gym)
    menu_kb = create_choice_trainer(trainers_id, gym)
    await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id, text='Выберите тренеров',
                                reply_markup=menu_kb)


@dp.callback_query_handler(lambda cb: cb.data.startswith('trainer'))
async def click_choice_trainer(cb: types.CallbackQuery):
    """
        Обработчик нажатия кнопок меню для добавления тренеров
    """
    click = cb.data.split('_')[1]
    gym = cb.data.split('_')[2]
    save_data = cb.data.split('_')[1]
    telegram_id = cb.from_user.id

    if "✅ " not in cb.data.split('_')[1]:
        save_trainer_in_user(save_data, telegram_id)
    else:
        delete_data = ' '.join(cb.data.split('_')[1].split(' ')[1:])
        delete_trainer_in_user(delete_data, telegram_id)

    trainers_id = get_id_trainers(gym)
    if click in selected_trainers:
        delete_excess_click_in_choice_trainer(click)
        selected_trainers.remove(click)
    else:
        selected_trainers.add(click)
        delete_excess_click_in_choice_trainer(click)
    keyboard = create_choice_trainer(trainers_id, gym)
    try:
        await bot.edit_message_reply_markup(chat_id=cb.from_user.id, message_id=cb.message.message_id,
                                            reply_markup=keyboard)
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda cb: cb.data.startswith('save_trainer'))
async def save_trainer_button(cb: types.CallbackQuery):
    menu_kb = create_record_del_record_menu()
    await bot.edit_message_text(chat_id=cb.from_user.id, message_id=cb.message.message_id, text='Главное меню',
                                reply_markup=InlineKeyboardMarkup())
    await bot.send_message(chat_id=cb.from_user.id, text='Сделайте выбор', reply_markup=menu_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('ignore'))
async def calendar_empty_days(cb: types.CallbackQuery):
    """
        Функция заглушка, что бы не висело сверху надпись "загрузка"
    """
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
        update_user_save(telegram_id, tr_id)


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
