from aiogram import types
from db import *
from settings import *


def start_command_btn():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_tasks = types.KeyboardButton(text=bot_text['start_btn'][0])
    button_add = types.KeyboardButton(text=bot_text['start_btn'][1])
    keyboard.add(button_tasks, button_add)
    return keyboard


def add_1_command_btn():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_morning = types.KeyboardButton(text=bot_text['add_1_btn'][0])
    button_evening = types.KeyboardButton(text=bot_text['add_1_btn'][1])
    button_urgently = types.KeyboardButton(text=bot_text['add_1_btn'][2])
    button_menu = types.KeyboardButton(text=bot_text['add_1_btn'][3])
    keyboard.add(button_morning, button_evening, button_urgently)
    keyboard.add(button_menu)
    return keyboard


def menu_btn():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_menu = types.KeyboardButton(text=bot_text['add_1_btn'][3])
    keyboard.add(button_menu)
    return keyboard


def tasks_btn():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_delete = types.KeyboardButton(text=bot_text['check_task_btn'][0])
    button_menu = types.KeyboardButton(text=bot_text['check_task_btn'][1])
    keyboard.add(button_delete, button_menu)
    return keyboard


def add_3_btn(data):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    places = []
    for obj in data:
        if obj[4] not in places:
            places.append(obj[4])
    for i in range(0, len(places), 2):
        btn1 = types.KeyboardButton(places[i])
        if i + 1 == len(places):
            keyboard.add(btn1)
        else:
            btn2 = types.KeyboardButton(places[i + 1])
            keyboard.add(btn1, btn2)
    button_menu = types.KeyboardButton(text=bot_text['add_1_btn'][3])
    keyboard.add(button_menu)
    return keyboard
