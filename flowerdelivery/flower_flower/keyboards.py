from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Список заказов', callback_data='see_orders'),

    ]
]
)
