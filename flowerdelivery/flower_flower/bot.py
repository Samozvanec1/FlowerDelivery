import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F
import asyncio
from .models import User, Flower, Order
from concurrent.futures import ThreadPoolExecutor
from asgiref.sync import sync_to_async

from .keyboards import start_keyboard

executor = ThreadPoolExecutor()

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Bot token
token = ''

# Initialize bot and dispatcher
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

# Define states
class Form(StatesGroup):
    name = State()
    email = State()
    tg_id = State()

def get_orders(user_id):
    # Adjust the fields as per the actual model fields
    return list(Order.objects.filter(user_id=user_id).values('flower_id', 'id'))

async def find_order(user_id):
    return await sync_to_async(get_orders)(user_id)

# Start command handler
@dp.callback_query(lambda c: c.data == 'see_orders')
async def see_orders(callback: CallbackQuery):
    user_id = callback.from_user.id  # assuming user ID is used to fetch orders
    try:
        user = await sync_to_async(User.objects.get)(tg_id=user_id)
        orders = await find_order(user)
        if orders:
            responce = f"Ваши заказы: \n"
            for order in orders:
                flower = await sync_to_async(Flower.objects.get)(pk=order['flower_id'])
                responce += f"Заказ на {flower.title} - {flower.price} \n"

        else:
            response = "Заказы не найдены😴."
    except Exception as e:
        response = "Произошла ошибка при получении заказов."

    # Edit the message with the formatted orders
    await callback.message.answer(str(responce))
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user_exists = await sync_to_async(User.objects.filter(tg_id=message.from_user.id).exists)()
    if not user_exists:
        await message.answer(f'Привет, {message.from_user.full_name}. Введи твоё настоящее имя')
        await state.set_state(Form.name)
    else:
        # Define the synchronous operation
        def get_all_flowers():
            return list(Flower.objects.all())

        # Run the synchronous operation in a thread
        loop = asyncio.get_event_loop()
        flowers = await loop.run_in_executor(executor, get_all_flowers)

        # Create the keyboard
        await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=start_keyboard)
@dp.message(Form.name)
async def handle_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Теперь введи свою почту')
    await state.set_state(Form.email)

# Email handler
@dp.message(Form.email)
async def handle_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()

    # Define the synchronous operation
    def create_user():
        User.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            tg_id=message.from_user.id
        )

    # Run the synchronous operation in a thread
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, create_user)

    await message.answer('Данные сохранены!')
    await state.clear()
# Start bot
async def start_bot():
    print('Бот запущен')
    await dp.start_polling(bot)

# Delete webhook
async def delete_webhook():
    await bot.delete_webhook()
    await bot.session.close()