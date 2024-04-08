from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='Искать 🔍', callback_data='button1')
b2 = InlineKeyboardButton(text='Редактировать ✏', callback_data='btn3')
kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[b1, b2]])