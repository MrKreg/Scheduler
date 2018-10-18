import pytz

TOKEN = '656003816:AAHATXcjF5-8ckXz-zSa60_NKa9KMJKcs44'

DBNAME = 'telegaBot.db'

COMMANDS = {
    'start': 'початок роботи з ботом',
    'help': 'переглянути список команд',
    'change': 'змінити групу',
    'check': 'перевірити, яку групу ти обрав'
}

RINGSCHEDULE = {1: '_8:00-9:20_',
                2: '_9:30-10:50_',
                3: '_11:10-12:30_',
                4: '_12:40-14:00_',
                5: '_14:10-15:30_',
                6: '_15:40-17:00_',
                7: '_17:10-18:30_'
                }

UKRAINE = pytz.timezone('Europe/Kiev')
