from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

#kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

button_1: KeyboardButton = KeyboardButton(text='Старт')
button_2: KeyboardButton = KeyboardButton(text='Правила')

keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]],
                                                       resize_keyboard=True)

#kb_builder.row(button_1, button_2, width=2)

#kb_builder: ReplyKeyboardMarkup = kb_builder.as_markup(one_time_keyboard=True,resize_keyboard=True)

