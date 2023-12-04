from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor
import logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from project1.models import ModelYroslav

logging.basicConfig(level=logging.INFO)

bot = Bot(token="your_bot_token")
dp = Dispatcher(storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
token =''

user_data = {}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Для регистрации введите /register")

@dp.message_handler(commands=['register'])
async def register_command(message: types.Message):
    await message.answer("Введите ваше имя")

    await ModelYroslav.waiting_for_name.set()

@dp.message_handler(state=ModelYroslav.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):

    user_data['name'] = message.text
    await message.answer("Теперь введите вашу почту")

    await ModelYroslav.waiting_for_email.set()

@dp.message_handler(state=ModelYroslav.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):

    user_data['email'] = message.text
    await message.answer("Теперь введите ваш пароль")

    await ModelYroslav.waiting_for_password.set()

@dp.message_handler(state=ModelYroslav.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):

    user_data['password'] = message.text

    your_model_instance = ModelYroslav(name=user_data['name'], email=user_data['email'], password=user_data['password'])
    your_model_instance.save()
    await message.answer("Вы успешно зарегистрированы!")

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
