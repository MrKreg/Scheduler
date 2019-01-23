import telebot
from telebot import types
from telebot.types import Message
from config import *
from datetime import datetime
import python_scheduler
from config import COMMANDS

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    print(message.from_user)
    if message.from_user.last_name is not None and message.from_user.first_name is not None:
        name = message.from_user.first_name + ' ' + message.from_user.last_name
    elif message.from_user.username is not None:
        name = message.from_user.username
    else:
        name = 'Незнайомець'
    msg = bot.send_message(message.chat.id,'Вітаю ' + name + '.')
    bot.register_next_step_handler(msg, new_student)


@bot.message_handler(commands=['help', 'info'])
def help_command(message: Message):
    help_text = 'Ти можеш використовувати такі команди: \n'
    for key in COMMANDS:
        help_text += '/' + key + ' : '
        help_text += COMMANDS[key] + '\n'
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['clr'])
def hide_buttons(message: Message):
    bot.send_message(message.chat.id, datetime.now().isoweekday(), reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['week'])
def week_command(message: Message):
    bot.send_message(message.chat.id, str(python_scheduler.get_week(datetime.now(tz=UKRAINE))) + ' тиждень')


@bot.message_handler(commands=['rings'])
def switch_rings(message: Message):
    if python_scheduler.RINGS == RINGSCHEDULE:
        python_scheduler.RINGS = SHORTEDRINGSSCHEDULE
    else:
        python_scheduler.RINGS = RINGSCHEDULE
    bot.send_message(message.chat.id, 'Успішно!')


@bot.message_handler(commands=['test'])
def test_command(message: Message):
    if not python_scheduler.is_user_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Обери групу:', reply_markup=choose_group_menu())
        bot.register_next_step_handler(message, new_student)
    schedule = python_scheduler.get_tomorrow_schedule(get_user(message.chat.id))
    line = ''
    for sub in schedule:
        line += str(sub)
    bot.send_message(message.chat.id, line, parse_mode='Markdown')


@bot.message_handler(commands=['change'])
def change_command(message: Message):
    if not python_scheduler.is_user_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Обери групу:', reply_markup=choose_group_menu())
        bot.register_next_step_handler(message, new_student)
    msg = bot.send_message(message.chat.id, 'Обери групу:', reply_markup=choose_group_menu())
    bot.register_next_step_handler(msg, update_student)


@bot.message_handler(commands=['check'])
def check_command(message: Message):
    if not python_scheduler.is_user_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Обери групу:', reply_markup=choose_group_menu())
        bot.register_next_step_handler(message, new_student)
        return
    group = python_scheduler.get_user(message.from_user.id)
    bot.send_message(message.chat.id,
                     'Ти обрав(ла) групу *' + group + '*.', parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def text_checker(message: Message):
    if not python_scheduler.is_user_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Обери групу:', reply_markup=choose_group_menu())
        bot.register_next_step_handler(message, new_student)
        return
    global response
    text = str(message.text)
    if text == 'Сьогодні':
        schedule = python_scheduler.get_today_schedule(python_scheduler.get_user(message.chat.id))
        response = prepare_schedule(schedule)
    elif text == 'Завтра':
        schedule = python_scheduler.get_tomorrow_schedule(python_scheduler.get_user(message.chat.id))
        response = prepare_schedule(schedule)
    elif text == 'Тиждень':
        schedule = python_scheduler.get_current_week_schedule(python_scheduler.get_user(message.chat.id))
        i = datetime.now(tz=UKRAINE).isoweekday()
        for day in schedule:
            response = WEEKDAYS[i] + '\n' + prepare_schedule(day)
            i += 1
            bot.send_message(message.chat.id, response, parse_mode='Markdown')
        return
    elif text == 'Розклад дзвінків':
        response = prepare_ring_schedule()
    else:
        response = 'Така команда мені невідома('
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


def new_student(message: Message):
    if message.text not in python_scheduler.get_all_groups():
        msg = bot.send_message(message.chat.id, 'Хитрий, да? Обери будь ласка групу із списку внизу)')
        bot.register_next_step_handler(msg, new_student)
        return
    if python_scheduler.create_user(message.from_user.id, message.text) == 201:
        bot.send_message(message.chat.id, 'Тепер ти можеш користуватися моїми можливостями)', reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, 'Ти можеш змінити групу за допомогою команди /change',
                         reply_markup=main_menu())


def update_student(message: Message):
    if not python_scheduler.is_user_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Обери групу:', reply_markup=choose_group_menu())
        bot.register_next_step_handler(message, new_student)
        return
    if message.text not in python_scheduler.get_all_groups():
        msg = bot.send_message(message.chat.id, 'Хитрий, да? Обери будь ласка групу із списку внизу)')
        bot.register_next_step_handler(msg, update_student)
        return
    if python_scheduler.update_user(message.from_user.id, message.text) == 200:
        bot.send_message(message.chat.id, 'Групу успішно змінено)', reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, 'Здається щось пішло не так(', reply_markup=main_menu())


def choose_group_menu():
    markup = types.ReplyKeyboardMarkup()
    for group in python_scheduler.get_all_groups():
        markup.add(types.KeyboardButton(group))
    return markup


def main_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Сьогодні', 'Завтра')
    markup.row('Тиждень', 'Розклад дзвінків')
    return markup


def prepare_schedule(schedule):
    line = ''
    for sub in schedule:
        line += str(sub)
    return line


def prepare_ring_schedule():
    line = ''
    for i in range(1, 8):
        line += '*' + str(i) + ' пара* ' + python_scheduler.RINGS[i] + '\n'
    return line


bot.polling(timeout=40)
