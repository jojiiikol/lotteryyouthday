from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_check_subscribe_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscribe")
    )
    return keyboard.as_markup()

def get_sex_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="👨 Мужской", callback_data="sex_male"),
        InlineKeyboardButton(text="👩 Женский", callback_data="sex_female")
    )
    return keyboard.adjust(2).as_markup()


def lottery_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="Выявить победителя")
    )
    return keyboard.as_markup(resize_keyboard=True)
