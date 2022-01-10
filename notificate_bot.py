import _thread
import asyncio
import datetime
import threading
import time
from operator import itemgetter
import sentry_sdk
import schedule
import telebot

import create_docx
from db import get_all_tasks, update_task
from settings import *
sentry_sdk.init(SENTRY_TOKEN, traces_sample_rate=1.0)
bot = telebot.TeleBot(token=TELEGRAM_BOT_SENDER_BOT)
messages_id = []


@bot.callback_query_handler(func=lambda call: call.data)
def cb_answer(obj):
    try:
        update_task(obj.data, 1, sentry_sdk)
    except:
        pass
    try:
        bot.delete_message(obj.message.chat.id, obj.message.id)
    except:
        pass


def get_tasks(type, task_type):
    data = asyncio.run(get_all_tasks(sentry_sdk))
    arr = []
    for obj in data:
        if type == obj[1]:
            if task_type == 'standart' or (task_type == 'alert' and obj[5] == 0):
                arr.append(obj)
    arr = sorted(arr, key=itemgetter(4))
    if len(arr) == 0:
        return []
    final_arr = [[arr[0]]]
    for i in range(1, len(arr)):
        if arr[i - 1][4] == arr[i][4]:
            final_arr[len(final_arr) - 1].append(arr[i])
        else:
            final_arr.append([arr[i]])
    return final_arr


def notification(type, task_type):
    if task_type == 'standart':
        messages_id.append(bot.send_message(CHANNEL_NAME, f'*Задачи на {type}\n{datetime.datetime.now().strftime("%d.%m.%Y [%H:%M]")}:*',
                         parse_mode="Markdown").message_id)
    else:
        delete_all_messages()
        messages_id.append(bot.send_message(CHANNEL_NAME, f'*Остались невыполненные задачи на {type}!*', parse_mode="Markdown").message_id)
    tasks = get_tasks(type, task_type)
    place = ''
    for i in tasks:
        for j in i:
            if place != j[4]:
                place = j[4]
                messages_id.append(bot.send_message(CHANNEL_NAME, "Место: _" + place + "_", parse_mode="Markdown").message_id)
            markup = telebot.types.InlineKeyboardMarkup(row_width=3)
            markup.row(telebot.types.InlineKeyboardButton('Выполнить', callback_data=j[0]), )
            messages_id.append(bot.send_message(CHANNEL_NAME, "Задание: " + j[3], reply_markup=markup).message_id)


def notification_morning():
    notification("Утро", 'standart')


def notification_evening():
    notification("Вечер", 'standart')


def delete_all_messages():
    global messages_id
    for m in messages_id:
        try:
            bot.delete_message(CHANNEL_NAME, m)
        except:
            pass
    messages_id = []


def send_document():
    d = create_docx.main(get_tasks('Утро', 'standart'), get_tasks("Вечер", 'standart'))
    bot.send_document(CHANNEL_NAME, open(d, 'rb'))


def life_cycle():
    schedule.every().day.at("09:00").do(notification_morning)
    schedule.every().day.at("22:30").do(notification_evening)

send_document()
exit(0)
_thread.start_new_thread(notification_evening, ())
time.sleep(3)
delete_all_messages()
#notification("Вечер", "alert")
bot.polling()
#while True:
#    schedule.run_pending()
#    time.sleep(1)