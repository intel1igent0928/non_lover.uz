# bot/keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.strings import TEXTS

def get_language_kb():
    buttons = [
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="lang_uz")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_main_menu(lang='ru'):
    buttons = [
        [
            KeyboardButton(text=TEXTS[lang]['btn_about']), 
            KeyboardButton(text=TEXTS[lang]['btn_free'])
        ],
        [
            KeyboardButton(text=TEXTS[lang]['btn_buy']), 
            KeyboardButton(text=TEXTS[lang]['btn_admin'])
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_admin_keyboard(user_id):
    buttons = [
        [
            InlineKeyboardButton(text="Одобрить ✅", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton(text="Отклонить ❌", callback_data=f"decline_{user_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
