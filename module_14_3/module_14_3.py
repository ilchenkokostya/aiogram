from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from api_token import api

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb2 = InlineKeyboardMarkup()
btn = InlineKeyboardButton(text='Отмена ввода', callback_data='cancel')
kb2.add(btn)

kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
        ],
        [InlineKeyboardButton(text='Купить', callback_data='Купить')]
    ]
)

kb3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продукт1", callback_data="product_buying"),
            InlineKeyboardButton(text="Продукт2", callback_data="product_buying"),
            InlineKeyboardButton(text="Продукт3", callback_data="product_buying"),
            InlineKeyboardButton(text="Продукт4", callback_data="product_buying")
        ],
        [InlineKeyboardButton(text="Назад", callback_data="start")]
    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# ---=== START ===----
@dp.message_handler(text=['start', '/start'])
async def start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.username}! Я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.callback_query_handler(text=['start'])
async def start_command(call):
    await call.message.answer(f"Привет! Я бот помогающий твоему здоровью.",reply_markup=kb)
    await call.answer()


# ---=== CANCEL ===----
@dp.callback_query_handler(text=['cancel'], state='*')
async def cancel_command(call, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await call.message.reply('Вы прервали заполнение данных!')
    await call.answer()


@dp.callback_query_handler(text=['Купить'])
async def get_buying_list(call):
    with open('module_14_3/img/original_fcb01214-ed67-439a-a77d-d069f8232fe8.webp', "rb") as product_1:
        await call.message.answer_photo(product_1, f"Название: Product1 | Описание: Доппельгерц актив | Цена: {1 * 100}")
    with open("module_14_3/img/original_140d6fb0-b244-4148-a706-eaf41c723fe6.webp", "rb") as product_2:
        await call.message.answer_photo(product_2, f"Название: Product2 | Описание: Турбослим Альфа | Цена: {2 * 100}")
    with open("module_14_3/img/3398097.jpg", "rb") as product_3:
        await call.message.answer_photo(product_3, f"Название: Product3 | Описание: BIOSPHIN | Цена: {3 * 100}")
    with open("module_14_3/img/original_d4d20c05-5310-4151-b431-505b06538ee3.webp", "rb") as product_4:
        await call.message.answer_photo(product_4, f"Название: Product4 | Описание: Грин Слим | Цена: {4 * 100}")
    await call.message.answer("Выберите продукт для покупки:", reply_markup=kb3)
    await call.answer()


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


# ---=== ИНФО ===----
@dp.callback_query_handler(text=['formulas'])
async def set_age(call):
    await call.message.answer(
        'Для женщин: (10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) − 161')
    await call.message.answer(
        'Для мужчин: (10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) + 5',
        reply_markup=kb)
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
    await message.answer(f"(Для женщин) Ваша норма калорий: {calories} ккал в день", reply_markup=kb)

    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
