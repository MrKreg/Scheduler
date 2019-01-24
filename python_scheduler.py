import requests
from datetime import datetime, timedelta
from config import *
from decimal import Decimal, ROUND_CEILING

RINGS = RINGSCHEDULE

class Lesson:
    def __init__(self, lesson):
        self.number = lesson['number']
        self.subject = lesson['subject']
        self.teacher = lesson['teacher']
        self.classroom = lesson['classroom']

    def __str__(self):
        return '*' + str(self.number) + ' пара* ' + RINGS[self.number] + '\n_' + self.subject + '_  *' + self.teacher + '* _' + str(
            self.classroom) + '_\n'


def get_user(uid):
    response = requests.get(URL + 'users/' + str(uid))
    return response.json()['group']


def create_user(uid, group_name):
    params = {
        'pk': uid,
        'group': group_name
    }
    response = requests.post(URL + 'users/', data=params)
    return response.status_code


def update_user(uid, group_name):
    params = {
        'pk': uid,
        'group': group_name
    }
    response = requests.put(URL + 'users/' + str(uid), data=params)
    return response.status_code


def is_user_exist(uid):
    response = requests.get(URL + 'users/' + str(uid))
    if response.status_code == 200:
        return True
    else:
        return False


def get_week(date):
    return (Decimal((date - datetime(2018, 9, 2, tzinfo=UKRAINE)).days / 7).quantize(0, ROUND_CEILING) % 4)


def get_one_day_schedule(group_name, weekday, week):
    simplified_week = 5
    schedule = []
    if week > 4:
        week = 1
    elif week % 2 == 0:
        simplified_week = 6
    request = URL + 'lessons/?week=0&week={}&week={}&group_name={}&day={}'.format(week,simplified_week,group_name,weekday)
    response = requests.get(request)
    for lesson in response.json():
        schedule.append(Lesson(lesson))
    return schedule


def get_today_schedule(group_name):
    weekday = datetime.now(tz=UKRAINE).isoweekday()
    week = get_week(datetime.now(tz=UKRAINE))
    if weekday > 5:
        return 'Пар немає)'
    return get_one_day_schedule(group_name, weekday, week)
    
def get_tomorrow_schedule(group_name):
    weekday = datetime.now(tz=UKRAINE).isoweekday()
    week = get_week(datetime.now(tz=UKRAINE))
    if weekday > 4:
        return 'Пар немає)'
    return get_one_day_schedule(group_name, weekday + 1, week)

def get_current_week_schedule(group_name):
    weekday = datetime.now(tz=UKRAINE).isoweekday()
    week = get_week(datetime.now(tz=UKRAINE))
    if weekday > 5:
        return 'Пар немає)'
    weekschedule = []
    for i in range(weekday, 6):
        weekschedule.append(get_one_day_schedule(group_name, i, week))
    return weekschedule

def get_all_groups():
    response = requests.get(URL + 'groups/')
    groups = []
    for group in response.json():
        groups.append(group['name'])
    return groups