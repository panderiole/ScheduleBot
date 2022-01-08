from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from keyboards import *
from db import *
from settings import *
import sentry_sdk
import re
from operator import itemgetter


class Form(StatesGroup):
    task_type = State()
    task_date = State()
    task_title = State()
    task_place = State()


class Delete(StatesGroup):
    waiting_id = State()


bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
sentry_sdk.init(SENTRY_TOKEN, traces_sample_rate=1.0)


@dp.message_handler(lambda m: m.text == '/start' or m.text == bot_text['add_1_btn'][-1], state="*")
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(bot_text['start'], reply_markup=start_command_btn())


@dp.message_handler(lambda m: m.text == bot_text['start_btn'][1])
async def add_1_command(message: types.Message):
    await message.answer(bot_text['add_1'], reply_markup=add_1_command_btn())
    await Form.task_type.set()


@dp.message_handler(lambda m: m.text in bot_text['add_1_btn'], state=Form.task_type)
async def add_2_command(message: types.Message, state: FSMContext):
    await state.update_data(task_type=message.text)
    await Form.task_date.set()
    await message.answer(bot_text["add_2"], reply_markup=menu_btn())


@dp.message_handler(state=Form.task_date)
async def add_3_command(message: types.Message, state: FSMContext):
    res = re.search(TIME_REGULAR, message.text)
    if res is None:
        await message.answer(bot_text["add_error"], reply_markup=menu_btn())
    else:
        await state.update_data(task_date=res.group(0))
        await Form.task_place.set()
        await message.answer(bot_text["add_3"], reply_markup=add_3_btn(await get_all_tasks(sentry_sdk)))


@dp.message_handler(state=Form.task_place)
async def add_4_command(message: types.Message, state: FSMContext):
    await state.update_data(task_place=message.text)
    await Form.task_title.set()
    await message.answer(bot_text["add_4"], reply_markup=menu_btn())


@dp.message_handler(state=Form.task_title)
async def add_5_command(message: types.Message, state: FSMContext):
    await state.update_data(task_title=message.text)
    await write_task(await state.get_data(), sentry_sdk)
    await message.answer(bot_text['add_5'], reply_markup=menu_btn())  # here need to add sqlite db
    await state.finish()


@dp.message_handler(lambda m: m.text in bot_text['start_btn'][0])
async def check_task_command(message: types.Message):
    data = await get_all_tasks(sentry_sdk)
    answer_string = ""
    morning_data, evening_data, urgently_data = [], [], []
    for obj in data:
        if obj[1] == bot_text['add_1_btn'][0]:
            morning_data.append(obj)
        elif obj[1] == bot_text['add_1_btn'][1]:
            evening_data.append(obj)
        elif obj[1] == bot_text['add_1_btn'][2]:
            urgently_data.append(obj)
    morning_data = sorted(morning_data, key=itemgetter(4))
    evening_data = sorted(evening_data, key=itemgetter(4))
    urgently_data = sorted(urgently_data, key=itemgetter(4))
    data_sorted = morning_data + evening_data + urgently_data
    for obj in data_sorted:
        obj_string = f"ID: {obj[0]},\nМесто: {obj[4]}\nСообщение: {obj[3]},\nТип: {obj[1]},\nВремя: {obj[2]}\n-----------------------\n"
        if len(obj_string) + len(answer_string) >= 4096:
            await message.answer(answer_string)
            answer_string = ''

        answer_string += obj_string
    await message.answer(answer_string)
    await message.answer(bot_text['check_task'], reply_markup=tasks_btn())


@dp.message_handler(lambda m: m.text in bot_text['check_task_btn'][0])
async def delete_1_command(message: types.Message):
    await message.answer(bot_text['delete_task'], reply_markup=menu_btn())
    await Delete.waiting_id.set()


@dp.message_handler(state=Delete.waiting_id)
async def delete_2_command(message: types.Message, state: FSMContext):
    data = await get_all_tasks(sentry_sdk)
    for obj in data:
        if str(obj[0]) == message.text.strip():
            await state.finish()
            await delete_task(obj[0], sentry_sdk)
            await message.answer(bot_text['delete_task_success'], reply_markup=menu_btn())
            return  # here we are deleting
    await message.answer(bot_text['delete_task_error'], reply_markup=menu_btn())

if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp)
        except Exception as e:
            sentry_sdk.capture_message(f"[Schedule bot] Polling error!\nRestarting...\nDesc: {e}")
