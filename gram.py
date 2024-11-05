from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "7700680355:AAFHfbUpjkYIqlIdWxWM4QbIsffcrvdYkHY"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)