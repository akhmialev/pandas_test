from web.bd import *


def date_record(id_trainer):
    date = send_data(id_trainer)
    return {'date': date}


def time_record(id_trainer, date):
    time = send_time(id_trainer, date)
    time_sp = time[0].split('-')
    start_time = int(time_sp[0])
    end_time = int(time_sp[1])

    busy_time = check_record_time(id_trainer, date)
    time_lst = []

    for i in range(start_time, end_time + 1):
        time_lst.append(str(i))
    unique_element = sorted(list(set(time_lst) - set(busy_time)))

    time_chart = []
    for i in unique_element:
        time_chart.append(f"{i}:00-{int(i) + 1}:00")

    return {'time': time_chart}


def finish_record(id_user, id_trainer, date, time):
    if check_click(id_user, id_trainer):
        return {'message': 'вы уже записаны'}
    else:
        save_record_to_trainer(id_user, id_trainer, date, time)
        record_data = save_record_to_user(id_user, id_trainer, date, time)
        save_user_click(id_user, id_trainer)
        return {'message': record_data}
