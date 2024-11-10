from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from api_token import api

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb = InlineKeyboardMarkup()
kb2 = InlineKeyboardMarkup()

btn1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
btn2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
btn3 = InlineKeyboardButton(text='Отмена ввода', callback_data='cancel')
kb.add(btn1).insert(btn2)
kb2.add(btn3)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# ---=== START ===----
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=kb)


# ---=== CANCEL ===----
@dp.callback_query_handler(text=['cancel'], state='*')
async def cancel_command(call, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await call.message.reply('Вы прервали заполнение данных!')


# ---=== ИНФО ===----
@dp.callback_query_handler(text=['formulas'])
async def set_age(call):
    await call.message.answer(
        'Для женщин: (10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) − 161')
    await call.message.answer(
        'Для мужчин: (10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) + 5')
    await call.answer()


# ---=== ВОЗРАСТ ===----
@dp.callback_query_handler(text=['Calories', 'calories', 'Рассчитать'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:', reply_markup=kb2)
    await call.answer()
    await UserState.age.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=UserState.age)
async def check_input(message: types.Message):
    return await message.reply('Вы ввели не число, повторите ввод')


# ---=== РОСТ ===----
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)

    await message.answer('Введите свой рост (в см):', reply_markup=kb2)
    await UserState.growth.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=UserState.growth)
async def check_input(message: types.Message):
    return await message.reply('Вы ввели не число, повторите ввод')


# ---=== ВЕС ===----
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)

    await message.answer('Введите свой вес (в кг):', reply_markup=kb2)
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


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
