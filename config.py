import pytz

TOKEN = '656003816:AAHATXcjF5-8ckXz-zSa60_NKa9KMJKcs44'

URL = 'http://mrkreg.pythonanywhere.com/'

DBNAME = 'telegaBot.db'

COMMANDS = {
    'start': 'початок роботи з ботом',
    'help': 'переглянути список команд',
    'change': 'змінити групу',
    'check': 'перевірити, яку групу ти обрав'
}

RINGSCHEDULE = {
    1: '_8:00-9:20_',
    2: '_9:30-10:50_',
    3: '_11:10-12:30_',
    4: '_12:40-14:00_',
    5: '_14:10-15:30_',
    6: '_15:40-17:00_',
    7: '_17:10-18:30_'
}

SHORTEDRINGSSCHEDULE = {
    1: '_8:00-9:00_',
    2: '_9:10-10:10_',
    3: '_10:30-11:30_',
    4: '_11:40-12:40_',
    5: '_12:50-13:50_',
    6: '_14:00-15:00_',
    7: '_15:10-16:10_'
}

WEEKDAYS = {
    1: '*Понеділок*',
    2: '*Вівторок*',
    3: '*Середа*',
    4: '*Четвер*',
    5: '*П\'ятниця*',
    6: '*Субота*',
    7: '*Неділя*'
}

UKRAINE = pytz.timezone('Europe/Kiev')
