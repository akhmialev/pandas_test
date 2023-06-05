from web.bd import *
from web.checks import *


def date_record(id_trainer):
    date = send_data(id_trainer)
    return {'date': date}


def time_record(id_trainer, date):
    if check_id_trainer(id_trainer):
        if check_data(date):
            time = send_time(id_trainer, date)
            if time:
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
            return {'message': 'Invalid data. On this date, the coach has no more time '}
        return {'message': f'Invalid date. Your date: {date}, success format dd.mm'}
    return {'message': f'Invalid id_trainer'}

def finish_record(id_user, id_trainer, date, time):
    if check_user_id(id_user):
        if check_id_trainer(id_trainer):
            if check_time(time):
                if check_data(date):
                    if check_click(id_user, id_trainer):
                        return {'message': 'вы уже записаны'}
                    else:
                        save_record_to_trainer(id_user, id_trainer, date, time)
                        record_data = save_record_to_user(id_user, id_trainer, date, time)
                        save_user_click(id_user, id_trainer)
                        return {'message': record_data}
                return {'message': f'Invalid date. Your date: {date}, success format dd.mm'}
            return {'message': f'Invalid time. Your time: {time}, success format hours:minutes'}
        return {'message': f'Invalid id_trainer'}
    return {'message': f'Invalid id_user'}
