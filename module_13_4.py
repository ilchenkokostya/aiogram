from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

from api_token import api

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# ---=== START ===----
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.')

# ---=== CANCEL ===----
@dp.message_handler(commands=['cancel'], state='*')
async def cancel_command(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply('Вы прервали заполнение данных!')



# ---=== ВОЗРАСТ ===----
@dp.message_handler(text=['Calories', 'calories'])
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(lambda message: not message.text.isdigit(), state=UserState.age)
async def check_input(message: types.Message):
    return await message.reply('Вы ввели не число, повторите ввод')


# ---=== РОСТ ===----
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)

    await message.answer('Введите свой рост (в см):')
    await UserState.growth.set()

@dp.message_handler(lambda message: not message.text.isdigit(), state=UserState.growth)
async def check_input(message: types.Message):
    return await message.reply('Вы ввели не число, повторите ввод')


# ---=== ВЕС ===----
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)

    await message.answer('Введите свой вес (в кг):')
    await UserState.weight.set()

@dp.message_handler(lambda message: not message.text.isdigit(), state=UserState.weight)
async def check_input(message: types.Message):
    return await message.reply('Вы ввели не число, повторите ввод')


# ---=== формулу Миффлина - Сан Жеора  ===----
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories = int(10 * weight + 6.25 * growth - 5 * age + 5)
    await message.answer(f"(Для мужчин) Ваша норма калорий: {calories} ккал в день")

    calories = int(10 * weight + 6.25 * growth - 5 * age - 161)
    await message.answer(f"(Для женщин) Ваша норма калорий: {calories} ккал в день")

    await state.finish()




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
