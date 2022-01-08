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


class Form(StatesGroup):
    task_type = State()
    task_date = State()
    task_title = State()


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
        await Form.task_title.set()
        await message.answer(bot_text["add_3"], reply_markup=menu_btn())


@dp.message_handler(state=Form.task_title)
async def add_4_command(message: types.Message, state: FSMContext):
    await state.update_data(task_title=message.text)
    await write_task(await state.get_data(), sentry_sdk)
    await message.answer(bot_text['add_4'], reply_markup=menu_btn())  # here need to add sqlite db
    await state.finish()


if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp)
        except Exception as e:
            sentry_sdk.capture_message(f"[Schedule bot] Polling error!\nRestarting...\nDesc: {e}")
