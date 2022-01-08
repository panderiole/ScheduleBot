from aiogram import types
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
